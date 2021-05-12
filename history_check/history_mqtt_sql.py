import paho.mqtt.client as mqtt
import mariadb
import json
import sys 
import time
import datetime
i=0
hist=0
msg_hist=""
user_dt="root"
password_dt="password"
def sql_data(s):
    s="'"+s+"'"
    return s
def data_give(location,appliance,fromdate,todate):
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 json_data= " "
 i=0
 table_name="ROOM_CONTROLBOX_APPLIANCE"
 #date formatting
 d1 = datetime.datetime(int(str(fromdate[6])+str(fromdate[7])+str(fromdate[8])+str(fromdate[9])),int(str(fromdate[3])+str(fromdate[4])),int(str(fromdate[0])+str(fromdate[1])))
 d2 = datetime.datetime(int(str(todate[6])+str(todate[7])+str(todate[8])+str(todate[9])),int(str(todate[3])+str(todate[4])),int(str(todate[0])+str(todate[1])))
 cur.execute("SELECT * FROM "+table_name+" WHERE APPLIANCE="+sql_data(appliance)+"AND LOCATION="+sql_data(location))
 for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur:
  #checking the date
  d3 = datetime.datetime(int(str(DATE[6])+str(DATE[7])+str(DATE[8])+str(DATE[9])),int(str(DATE[3])+str(DATE[4])),int(str(DATE[0])+str(DATE[1])))
  if d1<=d3 and d3<=d2:
      
    json1='{ "DATE":"'+DATE+'","LOCATION":"'+LOCATION+'","APPLIANCE":"'+APPLIANCE+'","USERNAME":"'+CLIENT+'","ON_TIME":"'+ON_TIME+'","OFF_TIME":"'+OFF_TIME+'","TOTAL_ON_TIME":"'+TOTAL_ON_TIME+'" }'
    sr=json.loads(json1)
    js=json.dumps(sr)
    #print(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME)
    if i==0:
      json_data=js
      i=1
    else:  
     json_data=js+","+json_data
 if json_data==" ":
      json_data='{"LOCATION":"'+location+'","APPLIANCE":"'+appliance+'","STATUS" : "NO_HISTORY"}'
 json_data="[ "+json_data+" ]"
 json_data=json.loads(json_data)
 json_data=json.dumps(json_data)
 #print(json_data)
 return json_data
def on_message_history(client, userdata, message):
    global hist,msg_hist
    hist=1
    msg_hist=str(message.payload.decode("utf-8"))
    print("received message: " ,msg_hist)
    
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

client = mqtt.Client("subscriber")
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                  
client.connect(mqttBroker,1884) 

client.loop_start()

#history will be published to this topic so subscribe to this topic from mobile
client.publish("history/pub","datasend",2)

#publish the request as per json fromat from the mobile to this topic
client.subscribe("history/sub")
client.on_message=on_message_history 
print("hello")
while True:
 if hist==1:
    hist=0
    #msg_hist='{"Location": "Lobby","Appliance":"Light7","from_date":"30/04/2021","to_date":"29/05/2021"}'
    dict_obj=json.loads(msg_hist)
    username=str(dict_obj.get("Username"))
    accesskey=str(dict_obj.get("AccessKey"))
    location= str(dict_obj.get("Location"))
    appliance=str(dict_obj.get("Appliance"))
    from_date=str(dict_obj.get("from_date"))
    to_date=str(dict_obj.get("to_date"))
    sent=data_give(location,appliance,from_date,to_date)
    sent='{"Username":"'+username+'" ,"AccessKey":"'+accesskey+'","history":'+sent+'}'
    print(sent)
    
    client.publish("history/pub",sent)
    
    



client.loop_stop()




