import mariadb

import sys 
import time
from datetime import datetime
# Connect to MariaDB Platform

conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
cur = conn.cursor()
contacts = []
ssid_new="stijo"
password_new="stijojoseph"
ip_new="192.168.43.81"
dump=1
cur.execute("select * from GATEWAY_CONFIG")
for ssid,password,k in cur:
    for char in ssid:
     if char in " ?.!/;:":
        ssid.replace(char,'')
    if ssid==ssid_new:
     dump=0
    print(ssid,password,k)
if dump==1:   
 now = datetime.now()
 dt= now.strftime("%d/%m/%Y");
 cur.execute("INSERT INTO GATEWAY_CONFIG(SSID,PASSWORD,IP_ADDRESS) VALUES (?,?,?)",(ssid_new,password_new,ip_new))
 conn.commit()

#conn.commit() 
conn.close()