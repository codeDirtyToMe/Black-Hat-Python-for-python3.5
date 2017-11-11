#!/usr/bin/python3.5
#As of now, this is most definitely not gonna work. I've only just written it up.
#I haven't even tried running it yet. I need to write my own hex dump function.
#That'll end up being a seperate project that I'll need to finish before I can
#come back and finish it.

import sys, socket, threading

def serverLoop(localHost, localPort, remoteHost, remotePort, receiveStatus) :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try :
        server.bind((localHost, localPort))
    except :
        print("[!!] Failed to listen on %s:%d" %(localHost, localPort))
        print("[!!] Check other listening sockets or correct permissions")
        exit(1)

    print("[*] Listening on %s:%d" %(localHost, localPort))

    server.listen(5)
    while True :
        clientSocket, clientAddr = server.accept() #Multiple assignment.

        #Output local connection info.
        print("[*] Received incoming connection from %s:%d" %(clientAddr[0], clientAddr[1]))

        #Start a thread to talk to the remote host.
        proxyThread = threading.Thread(target=proxyHandler, args=(clientSocket, remoteHost, remotePort, receiveStatus))

        proxyThread.start()

def receiveFrom(connection) :
    buffer = ""

    #Set a 2 second timeout depending on your target. This may need to be adjusted.
    connection.settimeout(2)

    try :
        #Keep reading into the buffer until there's no more data or we time out.
        while True :
            data = connection.recv(4096)

            if not data :
                break

            buffer += data

    except :
        pass

    return buffer

def hexDump() : #I'm gonna write this myself instead of using what Justin Seitz used.
    pass

def responseHandler(buffer) :
    #Perform packet modifications.
    return buffer

def requestHandler(buffer) :
    #Perform packet modifications.
    return buffer

def proxyHandler(clientSocket, remoteHost, remotePort, receiveStatus) :
    #Connect to the remote host.
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect((remoteHost, remotePort))

    #Receive data from the remote end if necessary

    if receiveStatus :
        remoteBuffer = receiveFrom(remoteSocket)
        hexDump(remoteBuffer)

        #Send it to our response handler.
        remoteBuffer = responseHandler(remoteBuffer)

        #If we have data to send to our local client, sent it.
        if len(remoteBuffer) :
            print("[*] Sending %d bytes to localhost." % len(remoteBuffer))
            clientSocket.send(remoteBuffer)

    #Loop and read from local.
    #Send to remote, send to local.
    #Rinse, wash, repeat.
    while True :
        #Read from localhost.
        localBuffer = receiveFrom(clientSocket)

        if len(localBuffer) :
            print("[*] Received %d bytes from localhost." % len(localBuffer))
            hexDump(localBuffer)

            #Send it to the request handler.
            localBuffer = requestHandler(localBuffer)

            #Send off the data to the remote host.
            remoteSocket.send(localBuffer)
            print("[*] Sent to remote.")

            #Receive the response.
            remoteBuffer = receiveFrom(remoteSocket)

        if len(remoteBuffer) :
            print("[*] Received %d bytes from remote." % len(remoteBuffer))
            hexDump(remoteBuffer)

            #Send to our response handler.
            remoteBuffer = responseHandler(remoteBuffer)

            #Send the response to the local socket.
            clientSocket.send(remoteBuffer)
            print("[*] Sent to localhost.")

        #If no more data on either side, close the connections.
        if not len(localBuffer) or not len(remoteBuffer) :
            clientSocket.close()
            remoteSocket.close()
            print("[*] No more data. Closing connections.")
            break

def main() :
    #No argument parsing in this example. I'll probably add some later.
    if len(sys.argv[1:]) != 5 : #If there's not 5 pieces of data, print out a help message.
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [(True | False) for receive first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        exit(1)

    #Setup local listening parameters.
    localHost = sys.argv[1]
    localPort = sys.argv[2]

    #Setup remote target parameters.
    remoteHost = sys.argv[3]
    remotePort = sys.argv[4]

    #Decide on whether receiving data first or not.
    receiveStatus = sys.argv[5]

    if "True" in receiveStatus : #Change status to True or False instead of the string versions.
        receiveStatus = True
    else :
        receiveStatus = False

    #Spin listening socket.
    serverLoop(localHost, localPort, remoteHost, remotePort, receiveStatus)

main()
