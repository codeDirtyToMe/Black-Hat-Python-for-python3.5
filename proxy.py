#!/usr/bin/python3.5
"""This might actually work now. There's something weird going on with iptables that's preventing it from 
working on ubuntu."""

import sys, socket, threading, binascii

def serverLoop(localHost, localPort, remoteHost, remotePort, receiveStatus) :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try :
        server.bind((localHost, localPort))
    except :
        print("[!!] Failed to listen on %s:%d" %(localHost, localPort))
        print("[!!] Check other listening sockets or correct permissions")
        exit(1)

    server.listen(5)
    print("[*] Listening on %s:%d" % (localHost, localPort))

    while True :
        print("test")
        client, addr = server.accept() #Multiple assignment.
        print("test1")
        #Output local connection info.
        print("[*] Received incoming connection from %s:%d" %(addr[0], addr[1]))

        #Start a thread to talk to the remote host.
        proxyThread = threading.Thread(target=proxyHandler, args=(client, remoteHost, remotePort, receiveStatus))

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

def hexDump(byteString) :
    byteList = list(byteString.decode())
    hexString = binascii.hexlify(byteString).decode()
    hexList = list(hexString)

    doubleHexList = []
    x = int(0)
    while x is not len(hexList):  # Combine the list into pairs of integers.
        doubleHexList.insert(x, str(str(hexList[x]) + str(hexList[x + 1])))
        x = x + 2

    linesOfHex = float(len(doubleHexList) / int(16))
    y = int(0)
    z = int(0)
    hexPad = " "
    bitOffSet = int(0)
    while y < linesOfHex:
        bitOffSet = bitOffSet + len(doubleHexList[z:z + 16])
        hexBitOffSet = hex(bitOffSet)
        doubleHexString = " ".join(doubleHexList[z:z + 16])
        if len(doubleHexString) < 47: hexPad = hexPad * (48 - len(doubleHexString))
        print(str(hexBitOffSet) + " | " + str(doubleHexString) + str(hexPad) + " | " + str(
            "".join(byteList[z:z + 16])))
        y += 1
        z += 16

def responseHandler(buffer) :
    #Perform packet modifications.
    return buffer

def requestHandler(buffer) :
    #Perform packet modifications.
    return buffer

def proxyHandler(clientSocket, remoteHost, remotePort, receiveStatus) :
    #Connect to the remote host.
    print("test2")
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("test3")
    remoteSocket.connect((remoteHost, remotePort))

    #Receive data from the remote end if necessary

    if receiveStatus is True :
        remoteBuffer = receiveFrom(remoteSocket)
        print(remoteBuffer)
        print(type(remoteBuffer))
        exit(0)
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
    localPort = int(sys.argv[2])

    #Setup remote target parameters.
    remoteHost = sys.argv[3]
    remotePort = int(sys.argv[4])

    #Decide on whether receiving data first or not.
    receiveStatus = sys.argv[5]

    if "True" in receiveStatus : #Change status to True or False instead of the string versions.
        receiveStatus = True
    else :
        receiveStatus = False

    #Spin listening socket.
    serverLoop(localHost, localPort, remoteHost, remotePort, receiveStatus)

main()
