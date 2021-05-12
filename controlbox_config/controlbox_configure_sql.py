import paho.mqtt.client as mqtt
import time
import json
import mariadb
import sys 

user_dt="root"
password_dt="password"


i=0;
msg=''
def sql_data(s):
    s="'"+s+"'"
    return s


#SENDING DATA TO THE SQL TABLE
def sql_datasend(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new):
  #configure your databse username adn password here  
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 table_name="CONTROLBOX_CONFIG"
 dump=0
 device_change=1
 device='1'
 #if device=1 means database is empty so newly needed to be added
 cur.execute("select * from "+table_name)
 for room,device,appliance1,appliance2,appliance3,appliance4 in cur:
    
    
    if device==device_new :
        device_change=0
    if device==device_new and  appliance1!=appliance1_new or appliance2!=appliance2_new or appliance3!=appliance3_new or appliance4!=appliance4_new:    
     #checking if the device id already exists if it exists update the appliancename room etc
        dump=1

        
    print(room,device,appliance1,appliance2,appliance3,appliance4)
 print(device)
 
 if device_change==1 or device=='1':
   #if new device has came or no devices in database  
  cur.execute("INSERT INTO "+table_name+" (ROOM,DEVICE,APPLIANCE1,APPLIANCE2,APPLIANCE3,APPLIANCE4) VALUES (?,?,?,?,?,?)",(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new))
  conn.commit()
  print("inserted")
 if dump==1:
     #updating the remaining coloumns if the new device exist in table
     cur.execute("UPDATE CONTROLBOX_CONFIG SET ROOM="+sql_data(room_new)+",APPLIANCE1="+sql_data(appliance1_new)+",APPLIANCE2="+sql_data(appliance2_new)+",APPLIANCE3="+sql_data(appliance3_new)+",APPLIANCE4="+sql_data(appliance4_new)+" where DEVICE="+sql_data(device_new))
     conn.commit()
     print("updated")
 #conn.commit()
 conn.close()
def on_message(client, userdata, message):
    global i,msg
    i=1
    msg=str(message.payload.decode("utf-8"))
    #print("received message: " ,msg)

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")    
    
#CONNECTING TO THE DATABASE

conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
cur = conn.cursor()
contacts = []

dump=1
#READING THE TABLE ,TO GET THE IP ADDRESS TO SET THE MQTT BROKER IF IP ADDRESS NOT FOUND
#IN TABLE IT MEANS WIFI HASNOT BEEN CONFIGURED
cur.execute("select * from GATEWAY_CONFIG")
for ssid,password,ip_address in cur:
     dump=0
if dump==0:
 #DATA EXITS IN TABLE
 #enter the local username and password   
 user = "username"
 password = "password"   
 mqttBroker =ip_address
 print(ip_address)
 client = mqtt.Client("subscriber")
 client.username_pw_set(user, password=password)    #set username and password
 client.on_connect= on_connect                   
 client.connect(mqttBroker,1884) 
 client.loop_start()
 client.subscribe("configure/#")
 client.on_message=on_message 
 print("hello")
 while True:
    if i==1:
        print(msg)
        i=0
        #OBTAINIG THE REQUIRED DATA FROM JSON DATA
        dict_obj = json.loads(msg)
        print(dict_obj.get('Room'),dict_obj.get('Device'),dict_obj.get('Appliance1'),dict_obj.get('Appliance2'),dict_obj.get('Appliance3'),dict_obj.get('Appliance4'))
        sql_datasend(dict_obj.get('Room'),dict_obj.get('Device'),dict_obj.get('Appliance1'),dict_obj.get('Appliance2'),dict_obj.get('Appliance3'),dict_obj.get('Appliance4'))
 client.loop_stop()



