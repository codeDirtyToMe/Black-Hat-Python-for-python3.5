#!/usr/bin/python3.5
import threading, argparse, socket, sys, subprocess, os

# Creating the options and arguments
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--listen", help="[*]Listen for incoming connections.", action="store_true")
parser.add_argument("-e", "--execute", type=str, help="[*]Execute the given file upon receiving a connection.")
parser.add_argument("-c", "--commandshell", help="[*]Initialize a command shell.", action="store_true")
parser.add_argument("-u", "--upload", type=str, help="[*]Upon receiving a connection, upload a file and write to [destination].")
parser.add_argument("-t", "--target", type=str, help="[*]Specify target IP address.")
parser.add_argument("-p", "--port", type=int, help="[*]Specify target port.")
arguments = parser.parse_args()

listen = arguments.listen
command = arguments.commandshell
upload = arguments.upload
execute = arguments.execute
target = arguments.target
port = arguments.port

# Some other global variables
uploadDestination = ""

#Client Sender####################################################################################################
def clientSender(buffer) :
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        client.connect((target, port)) #Connect to tgt host.
        print("Connected")
        if len(buffer) > int(0) :
            client.send(buffer.encode())

        while True : #Wait for data to return.
            recvLength = 1
            response = "".encode()

            while recvLength :
                data = client.recv(4096)
                recvLength = int(len(data))
                response = response + data

                if recvLength < int(4096) :
                    break

            buffer = input(response) #Wait for more input.
            buffer = buffer + "\n"

            client.send(buffer.encode()) #Send it off.
    except :
        print("[*] Exception! Exiting.")
        client.close #Tear down the connection.

#Run Command####################################################################################################
def runCommand(command) :
    command = command.rstrip() #Trim the newline of ending white space.

    try : #Run the command and return output.
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except :
        output = "Failed to execute command.\r\n"

    return output

#Server Loop###################################################################################################
def serverLoop() :
    global port
    global target
    print("serverLoop")
    if target == None :
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    print("Listening on: " + str(target) + ":" + str(port))
    server.listen(5)

    while True :
        clientSocket, addr = server.accept()
        #Spin off a thread to handle new client.
        clientThread = threading.Thread(target=clientHandler, args=(clientSocket,))
        clientThread.start()

#Client Handler###############################################################################################
def clientHandler(clientSocket) :
    global upload
    global execute
    global command
    global uploadDestination

    if len(uploadDestination) : #Check for upload.
        fileBuffer = "" #Read in the bytes and write to destination.

        while True :
            data = clientSocket.recv(1024)

            if not data :
                break
            else :
                fileBuffer += data

        try : #Output the bytes.
            fileDescriptor = open(uploadDestination, "wb")
            fileDescriptor.write(fileBuffer)
            fileDescriptor.close()
            clientSocket.send("Successfully saved file to %s\r\n".encode() % uploadDestination)
        except :
            clientSocket.send("Failed to save file to %s\r\n".encode() % uploadDestination)

    if execute is not None : #Check for command execution.
        output = runCommand(execute) #Run the command.
        clientSocket.send(output)

    if command == True : #Command shell is requested.
        while True :
            clientSocket.send("<BHP:#> ".encode()) #Show a simple prompt.
            cmdBuffer = "".encode()

            while "\n".encode() not in cmdBuffer :
                cmdBuffer += clientSocket.recv(1024)

            response = runCommand(cmdBuffer) #Return command output.

            clientSocket.send(response) #Return response


# Main#############################################################################################################
def main():
    # Determine whether listening or sending. Insert catching or receiving joke here.
    if listen is not True and len(target) and port > 0 : #Sending
        print("<CTRL-D> to send commands: ")
        buffer = sys.stdin.read()  # Load buffer with input from CLI.
        clientSender(buffer)  # Send the data.

    elif listen is True : #Listening
        serverLoop() #Boot up listener.

    else :
        print("Error.")
        exit(1)

main()