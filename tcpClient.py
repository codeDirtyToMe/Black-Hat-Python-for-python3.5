#!/usr/bin/python3.5
import socket

targetHost = "www.google.com"
targetPort = 80

#create a socket object

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect the client
client.connect((targetHost,targetPort))

#send some data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode())

#receive some data
response = client.recv(4096).decode("utf-8")

print(response)