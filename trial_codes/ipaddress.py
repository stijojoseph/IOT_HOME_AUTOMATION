import os
import socket
import fcntl
import struct

def ipadd():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()

 print("ipaddress",ip_address)
ipadd() 