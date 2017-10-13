#!/usr/bin/python3.5
import socket

targetHost = "127.0.0.1"
targetPort = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("AAABBBCCC".encode(), (targetHost,targetPort))

data, addr = client.recvfrom(4096)

print(data)

exit(0)
