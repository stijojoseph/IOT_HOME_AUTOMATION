import paho.mqtt.client as mqtt
import time
import mariadb
import json
import sys 
import time
from datetime import datetime

def sql_data(s):
    s="'"+s+"'"
    return s

live=0
msg_live=""
def sql_datasend_livestatus(LOCATION_NEW,APPLIANCE_NEW):
 status="OFF"   
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 
 contacts = []
 table_name="ROOM_CONTROLBOX_APPLIANCE"
 dump=1
 cur = conn.cursor()
 app1=0
 app2=0
 app3=0
 app4=0
 loop=0
 exist=0
 json1=""
 json2=""
 if APPLIANCE_NEW=="All":
     cur.execute("SELECT * FROM CONTROLBOX_CONFIG")
     for room,device,appliance1,appliance2,appliance3,appliance4 in cur:
         
        print(room,device,appliance1,appliance2,appliance3,appliance4 )
        conn1 = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 
        cur1 = conn1.cursor()
        cur1.execute("select * from "+table_name+" where LOCATION="+sql_data(room)+"and APPLIANCE="+sql_data(appliance1)+"and OFF_TIME="+sql_data("NULL"))   
        
        for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur1: 
         json1='"'+device+'": [{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"},'
         exist=exist+1
         app1=1
         break
        if app1==0:
             json1='"'+device+'": [{ "location":"'+room+'","appliance":"'+appliance1+'","status": "OFF"},'
        cur1.execute("select * from "+table_name+" where LOCATION="+sql_data(room)+"and APPLIANCE="+sql_data(appliance2)+"and OFF_TIME="+sql_data("NULL"))   
        for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur1: 
         json1+='{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"},'
         exist=exist+1
         app2=1
         break
        if app2==0:
             json1+='{ "location":"'+room+'","appliance":"'+appliance2+'","status": "OFF"},' 
         
        cur1.execute("select * from "+table_name+" where LOCATION="+sql_data(room)+"and APPLIANCE="+sql_data(appliance3)+"and OFF_TIME="+sql_data("NULL"))   
        for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur1: 
         json1+='{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"},'
         exist=exist+1
         app3=1
         break
        if app3==0:
             json1+='{ "location":"'+room+'","appliance":"'+appliance3+'","status": "OFF"},'
        cur1.execute("select * from "+table_name+" where LOCATION="+sql_data(room)+"and APPLIANCE="+sql_data(appliance4)+"and OFF_TIME="+sql_data("NULL"))   
        for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur1: 
         json1+='{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"}]'
         exist=exist+1
         app4=1
         
         break
        if app4==0:
             json1+='{ "location":"'+room+'","appliance":"'+appliance4+'","status": "OFF"}]'
        if loop==0:
         json2="{"+json1+"}"
         loop=loop+1
        else:
         json2=json2+",{"+json1+"}"
        
        exist=0
        json1=""
        app1=0
        app2=0
        app3=0
        app4=0 
     json2="["+json2+"]"    
     status=json2          
 else:
   status='{ "location":"'+LOCATION_NEW+'","appliance":"'+APPLIANCE_NEW+'","status": "OFF"}'
   cur.execute("select * from "+table_name+" where LOCATION="+sql_data(LOCATION_NEW)+"and APPLIANCE="+sql_data(APPLIANCE_NEW)+"and OFF_TIME="+sql_data("NULL"))   
    
   for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur: 
    status='{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"}'
  # print(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME)     
 print(status)
 return status
     
print(sql_datasend_livestatus("Kitchen","Light2") )    
     
     

