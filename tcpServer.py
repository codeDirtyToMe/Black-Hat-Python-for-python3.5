#!/usr/bin/python3.5
import socket, threading

bindIP = "0.0.0.0"
bindPort = 999

#Client handling thread.
def handleClient(clientSocket) :
    #Output sending data
    request = clientSocket.recv(1024)
    print("[*] Received: %s" % request)

    #Response
    clientSocket.send("ACK!".encode())
    clientSocket.close()
                        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bindIP, bindPort))

server.listen(5)

print("[*] Listening on %s:%d" % (bindIP, bindPort))

while True :
    client,addr = server.accept() #Multiple assignment.
    print("[*] Accepted connection from: %s:%d" %(addr[0], addr[1]))

    #Spin up our client thread to handle incoming data.
    clientHandler = threading.Thread(target=handleClient,args=(client,))
    clientHandler.start()
