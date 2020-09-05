#!/bin/python
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP

file = open('Stardust-Logger.txt', 'r') 
Lines = file.readlines() 

for line in Lines: 
	sock.sendto(str.encode(line), (UDP_IP, UDP_PORT))
	print(line)
	time.sleep(1)