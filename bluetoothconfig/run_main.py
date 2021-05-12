#!/usr/bin/env python
#Run.py
"""THIS IS THE FIRST PYTHON FILE WHICH NEEDED TO BE EXECUTED OR TESTED IN ORDER

OBJECTIVE-
1.CONNECT THE RASPBERRY TO WIFI BY SENDING SSID AND PASSWORD VIA MOBILE BLUETOOTH
AND STORE IT IN SQL DATABASE OF RASPBERRY PI,
2.OBTAIN GATEWAY ADDRESS/IPADDRESS TO
MOBILEPHONE WHICH IS USED WHEN CONFIGURING ESP8266/CONTROL BOX CONFIGURATION IN THE WEBPAGE
3.SEND THE USERNAME,PASSWORD,SECURITYKEY FOR SQL DATABASE STORAGE

PROCEDURE
AFTER PAIRING OF MOBILE BLUETOOTH WITH RASPBERRY PI , CONNECT MOBILE BLUETOOTH TO
RASPBERRY PI BLUETOOTH,WE WILL BE SENDING SSID AND PASSWORD
OF THE WIFI WE NEED TO CONNECT

AFTER THIS IS SUCCESSFULL AGAIN A BLUETOOTH CHANNEL WILL CREATED FOR SENDING
USERNAME,PASSWORD,SECURITYKEY FOR SQL DATABASE STORAGE

IN THE APP TYPE YOUR WIFI'S SSID AND PASSWORD ,IN HERE RUN THIS FILE IN CMD




"""




import mariadb

import sys 
import time
from datetime import datetime
import os
from bluetooth import *
from wifi import Cell, Scheme
import subprocess
import time
import os
import socket
import fcntl
import struct
import ipaddress

user_dt="root"
password_dt="password"


wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "
ssid_new=''
password_new=''
ip_new=''
def sql_datasend(ssid_new,password_new,ip_new):
 """OPENING THE DATA"""
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []

 dump=1
 cur.execute("select * from GATEWAY_CONFIG")
 for ssid,password,k in cur:
    for char in ssid:
     if char in " ?.!/;:":
        ssid.replace(char,'')
    if ssid==ssid_new and password==password_new :
     dump=0
    print(ssid,password,k)
 if dump==1:   
  now = datetime.now()
  dt= now.strftime("%d/%m/%Y");
  cur.execute("DELETE  FROM GATEWAY_CONFIG")
  conn.commit()
  cur.execute("INSERT INTO GATEWAY_CONFIG(SSID,PASSWORD,IP_ADDRESS) VALUES (?,?,?)",(ssid_new,password_new,ip_new))
  conn.commit()

#conn.commit() 
 conn.close()
 

def wifi_connect(ssid, psk):
    # write wifi config to file
    
    cmd = 'wpa_passphrase {ssid} {psk} | sudo tee -a {conf} > /dev/null'.format(
            ssid=str(ssid).replace('!', '\!'),
            psk=str(psk).replace('!', '\!'),
            conf=wpa_supplicant_conf
        )
    cmd_result = ""
    cmd_result = os.system(cmd)
    #print( cmd + " - " + str(cmd_result))
    # reconfigure wifi
    cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
    cmd_result = os.system(cmd)
    #print( cmd + " - " + str(cmd_result))
    time.sleep(10)
    cmd = 'iwconfig wlan0'
    cmd_result = os.system(cmd)
   # print( cmd + " - " + str(cmd_result))
    time.sleep(10)
    cmd = 'ifconfig wlan0'
    cmd_result = os.system(cmd)
    #print( cmd + " - " + str(cmd_result))
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        ip_address = out
    else:
        ip_address = "<Not Set>"
        print("wifi not connected check ssid and password")
    
    ip_address=ip()
    #print("ipaddress------",ip_address)    
    return ip_address
def ip():
    ip_address = '';
    global ip_new,password_new,ssid_new
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    #print("ip -address",ip_address)
    print("data send to sql datbase")
    ip_new=ip_address
    sql_datasend(ssid_new,password_new,ip_new)
    return ip_address
def ssid_discovered():
    Cells = Cell.all('wlan0')
    wifi_info = 'Found ssid : \n'
    for current in Cells:
        wifi_info += current.ssid + "\n"
    wifi_info+="!"
    #print( wifi_info)
    return wifi_info
def ssid_check(ssid1):
    #checkimg the ssid recieved from bluetooth is matching with the ssid discovered through scanning
    count=0
    Cells = Cell.all('wlan0')
    wifi_info = 'Found ssid : \n'
    for current in Cells:
        if ssid1==current.ssid:
            count=1
        wifi_info += current.ssid + "\n"
    wifi_info+="!"
    #print( wifi_info)
    return count
def handle_client(client_sock) :
    # get ssid
    global ssid_new,password_new
    client_sock.send(ssid_discovered())
    print( "Waiting for SSID...")
    ssid = client_sock.recv(1024)
    ssid=ssid.decode('utf-8')
    ssid_new=ssid
    #IF RECIEVED BLANK SSID 
    if ssid == '' :
        return
    print( "ssid received")
    print( ssid)
    # get psk
    client_sock.send("waiting-psk!")
    print( "Waiting for PSK...")
    psk = client_sock.recv(1024)
    psk=psk.decode('utf-8')
    if psk == '' :
        return
    password_new=psk
    print( "psk received")
    print( psk)
    if ssid_check(ssid_new)==1:
     print("the recieved SSID matches with the discovered SSID ")
     print("*********wait for 15 seconds please******************") 
     ip_address = wifi_connect(ssid, psk)
    #ip_address=ip()
    #ip()
    
    #print( "ip address: " + ip_address)
    
     client_sock.send("ip-address:" + str(ip_address) + "!")
     client_sock.close()
     server_sock.close()
     cmd = 'python3 bluetooth_config_main.py'
     cmd_result = os.system(cmd)
    
    
     return
try:
    while True:
        print("wifi password configurations starting")
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)
        port = server_sock.getsockname()[1]
        uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"
        advertise_service( server_sock, "RPi Wifi config",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])
        print( "Waiting for connection on RFCOMM channel %d" % port)
        client_sock, client_info = server_sock.accept()
        print( "Accepted connection from ", client_info)
        handle_client(client_sock)
        client_sock.close()
        server_sock.close()
        #time.sleep(15);
        #cmd="python3 ipaddress.py"
        #cmd_result = os.system(cmd)
        #print cmd + " - " + str(cmd_result)
        #ip()
        # finished config
        print ('Finished configuration\n')
except (KeyboardInterrupt, SystemExit):
    print( '\nExiting\n')
