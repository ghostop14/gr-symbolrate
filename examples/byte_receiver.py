#!/usr/bin/python3

import socket
from functools import partial

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
udpport=6543
server_address = ('localhost', udpport)
print('starting up on port ', udpport)
sock.bind(server_address)

print('\nwaiting to receive message')
while True:
    data, address = sock.recvfrom(4096)
    
    if data:
        for byte in data:
            # ord_byte=ord(byte)

            if byte== 0:
                print('0',end="")
            elif byte== 1:
                print('1',end="")

    # print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    # print >>sys.stderr, data
    
