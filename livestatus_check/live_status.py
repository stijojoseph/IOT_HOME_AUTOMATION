import paho.mqtt.client as mqtt
import time
import mariadb
import json
import sys 
import time
from datetime import datetime
#database username and password
user_dt="root"
password_dt="password"

def sql_data(s):
    s="'"+s+"'"
    return s

live=0
msg_live=""
def sql_datasend_livestatus(LOCATION_NEW,APPLIANCE_NEW):
 status="OFF"   
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 
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
 #when all the appliances current status needed to be uploaded
 if APPLIANCE_NEW=="All":
     cur.execute("SELECT * FROM CONTROLBOX_CONFIG")
     #getting all appliance names from controlbox_config table
     for room,device,appliance1,appliance2,appliance3,appliance4 in cur:
         
        print(room,device,appliance1,appliance2,appliance3,appliance4 )
         
        conn1 = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 
        cur1 = conn1.cursor()
        #listing out the appliances connected to a device which is in on position
        cur1.execute("select * from "+table_name+" where LOCATION="+sql_data(room)+"and APPLIANCE="+sql_data(appliance1)+"and OFF_TIME="+sql_data("NULL"))   
        #checking the particular appliance status is on
        
        for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur1: 
         json1='"'+device+'": [{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"},'
         exist=exist+1
         app1=1
         break
        #if app=1 means appliance is on so no need to update status as OFF
        if app1==0:
            # json format making
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
     #print(json2)
     status=json2
 else:
   #checking the status of particular appliance  
   status='{ "location":"'+LOCATION_NEW+'","appliance":"'+APPLIANCE_NEW+'","status": "OFF"}'
   cur.execute("select * from "+table_name+" where LOCATION="+sql_data(LOCATION_NEW)+"and APPLIANCE="+sql_data(APPLIANCE_NEW)+"and OFF_TIME="+sql_data("NULL"))   
    
   for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur: 
    status='{ "location":"'+LOCATION+'","appliance":"'+APPLIANCE+'","status": "ON"}'
  # print(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME)     
 
 return status
     
     
     
     
     
def on_message_live(client, userdata, message):
    global live,msg_live
    live=1
    msg_live=str(message.payload.decode("utf-8"))
    
    
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")    
    
user = "username"
password = "password"    
mqttBroker ="192.168.43.81"

client = mqtt.Client("subscriber",2)
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                  
client.connect(mqttBroker,1884,2) 

client.loop_start()
client.publish("live/pub","datasend",2)
client.subscribe("livestatus/#")
client.on_message=on_message_live 
print("hello")
while True:
 if live==1:
     live=0
     print(msg_live+"\n \n")
     #extarcting json data
     dict_obj = json.loads(msg_live)
     username=str(dict_obj.get("Username"))
     accesskey=str(dict_obj.get("AccessKey"))
     #senting to database
     sent=sql_datasend_livestatus(dict_obj.get("location"),dict_obj.get("appliance"))
     sent='{"Username":"'+username+'" ,"AccessKey":"'+accesskey+'","status":'+sent+'}'
     print("\n \n"+sent)
     client.publish("live/pub",sent)
client.loop_stop()