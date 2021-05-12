import mariadb

import sys 
import time
from datetime import datetime
# Connect to MariaDB Platform
def sql_data(s):
    s="'"+s+"'"
    return s
def sql_datasend(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new):
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 table_name="CONTROLBOX_CONFIG"
 dump=0
 device_change=1
 device='1'
 print("came")
 cur.execute("select * from "+table_name)
 for room,device,appliance1,appliance2,appliance3,appliance4 in cur:
    #for char in room:
     #if char in " ?.!/;:":
      #  room.replace(char,'')
    if device==device_new :
        device_change=0
    if device==device_new and  appliance1!=appliance1_new or appliance2!=appliance2_new or appliance3!=appliance3_new or appliance4!=appliance4_new:    
     
        dump=1

        
    print(room,device,appliance1,appliance2,appliance3,appliance4)
 print(device)
 
 if device_change==1 or device=='1':   
  cur.execute("INSERT INTO "+table_name+" (ROOM,DEVICE,APPLIANCE1,APPLIANCE2,APPLIANCE3,APPLIANCE4) VALUES (?,?,?,?,?,?)",(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new))
  conn.commit()
  print("inserted")
 if dump==1:
     cur.execute("UPDATE CONTROLBOX_CONFIG SET ROOM="+sql_data(room_new)+",APPLIANCE1="+sql_data(appliance1_new)+",APPLIANCE2="+sql_data(appliance2_new)+",APPLIANCE3="+sql_data(appliance3_new)+",APPLIANCE4="+sql_data(appliance4_new)+" where DEVICE="+sql_data(device_new))
     conn.commit()
     print("updated")
 #conn.commit()
 conn.close()
 
room_new='Kitchen'
device_new="Device2"
appliance1_new="Light1"
appliance2_new="Light5"
appliance3_new="Fan1"
appliance4_new="Light3"
sql_datasend(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new)
