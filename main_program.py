import paho.mqtt.client as mqtt
import time
import json
import mariadb
import sys
import time
import datetime

user_dt="root"
password_dt="password"


ackn=0
i=0;
msg=''
live=0
msg_live=""


def timer():
 
 now = datetime.now()
 datenow= now.strftime("%d/%m/%Y")
 timenow=now.strftime("%H:%M:%S")
 #print("date and time =", datenow,timenow)
 
def difference(h1, m1, h2, m2):
      
    # convert h1 : m1 into
    # minutes
    t1 = h1 * 60 + m1
      
    # convert h2 : m2 into
    # minutes 
    t2 = h2 * 60 + m2
      
    
    diff=t2-t1  
        # calculating the difference
    
      
        
        
    # calculating hours from
    # difference
    h = (int(diff / 60)) % 24
      
    # calculating minutes from 
    # difference
    m = diff % 60
  
    #print(h, ":", m)
    return h,m
#difference(22,40,10,10)
 
# Python3 program two find number of
# days between two given dates

# A date has day 'd', month 'm' and year 'y'


class Date:
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.y = y


# To store number of days in all months from
# January to Dec.
monthDays = [31, 28, 31, 30, 31, 30,
			31, 31, 30, 31, 30, 31]

# This function counts number of leap years
# before the given date


def countLeapYears(d):

	years = d.y

	# Check if the current year needs to be considered
	# for the count of leap years or not
	if (d.m <= 2):
		years -= 1

	# An year is a leap year if it is a multiple of 4,
	# multiple of 400 and not a multiple of 100.
	return int(years / 4) - int(years / 100) + int(years / 400)


# This function returns number of days between two
# given dates
def getDifference(dt1, dt2):

	# COUNT TOTAL NUMBER OF DAYS BEFORE FIRST DATE 'dt1'

	# initialize count using years and day
	n1 = dt1.y * 365 + dt1.d

	# Add days for months in given date
	for i in range(0, dt1.m - 1):
		n1 += monthDays[i]

	# Since every leap year is of 366 days,
	# Add a day for every leap year
	n1 += countLeapYears(dt1)

	# SIMILARLY, COUNT TOTAL NUMBER OF DAYS BEFORE 'dt2'

	n2 = dt2.y * 365 + dt2.d
	for i in range(0, dt2.m - 1):
		n2 += monthDays[i]
	n2 += countLeapYears(dt2)

	# return difference between two counts
	return (n2 - n1)


# Driver program
#dt1 = Date(10, 12, 2018)
#dt2 = Date(25, 2, 2019)

#print(getDifference(dt1, dt2), "days")
def time_convert(time):
    return int(time[0])*10+int(time[1]),int(time[3])*10+int(time[4])
def date_convert(time):
    #print(time)
    return int(time[0])*10+int(time[1]),int(time[3])*10+int(time[4]),int(time[6])*1000+int(time[7])*100+int(time[8])*10+int(time[9])
    

def sql_datasend_ack(LOCATION_NEW,CLIENT_NEW,APPLIANCE_NEW,STATE):
 from datetime import datetime   
 insert="1"
 update="0"
 now = datetime.now()
 #datenow="03/05/2021" #now.strftime("%d/%m/%Y")
 #timenow="23:30:23"#now.strftime("%H:%M:%S")
 datenow=now.strftime("%d/%m/%Y")
 timenow=now.strftime("%H:%M:%S")
 print("date and time =", datenow,timenow)
 DATE=datenow
 ON_TIME_NEW="NULL"
 OFF_TIME_NEW="NULL"
 TOTAL_ON_TIME_NEW="NULL"
 old_on_date="NULL"
 old_on_time="NULL"
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 table_name="ROOM_CONTROLBOX_APPLIANCE"
 dump=1
 cur.execute("select * from "+table_name)
 for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur:
    if LOCATION==LOCATION_NEW and APPLIANCE==APPLIANCE_NEW and OFF_TIME=="NULL": 
        if STATE=="1":
            insert="0"
            ON_TIME_NEW=timenow
        else:
           update="1"     
           OFF_TIME_NEW=timenow 
           old_on_time=ON_TIME 
           old_on_date=DATE
        
 if insert=="1" and STATE=="1":
    print("inserted")   
    cur.execute("INSERT INTO "+table_name+"(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME) VALUES (?,?,?,?,?,?,?)",(datenow,LOCATION_NEW,CLIENT_NEW,APPLIANCE_NEW,timenow,"NULL","NULL"))   
    conn.commit()
 if update=="1":
    print("updated")
    time1=old_on_time
    time2=timenow
    #print(time1,time2)
    s,r=time_convert(time1)
    p,k=time_convert(time2)
#print(s,r,p,k)
    hr,mins=difference(s,r,p,k)
    #print(timer)
    date1=old_on_date
    date2=datenow
    a,b,c=date_convert(date1)
    d,e,f=date_convert(date2)
#print(a,b,c,d,e,f)
    print(date2)
    dt1 = Date(a,b,c)
    if int(s)>int(p):
     dt2 = Date(d-1,e,f)
    else:
       dt2 = Date(d,e,f) 
    date_hr=getDifference(dt1, dt2)*24
    
    total_hrs=str(str(date_hr+hr)+"HRS"+str(mins)+"MINS")
    print(total_hrs)
    cur.execute("UPDATE "+ table_name +" SET OFF_TIME="+sql_data(timenow)+",TOTAL_ON_TIME="+sql_data(total_hrs)+" where APPLIANCE="+sql_data(APPLIANCE_NEW)+" and LOCATION="+sql_data(LOCATION_NEW)+" and ON_TIME="+ sql_data(old_on_time)) 
    conn.commit()
  #cur.execute("INSERT INTO "+table_name+"(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME) VALUES (?,?,?,?,?.?.?)",(DATE,LOCATION_NEW,CLIENT_NEW,APPLIANCE_NEW,ON_TIME_NEW,OFF_TIME_NEW,TOTAL_ON_TIME_NEW))
  #cur.execute(" UPDATE GATEWAY_CONFIG SET PASSWORD="+password_new+",SSID='stijojoseph' where IP_ADDRESS="+ip_new)
  #conn.commit()

#conn.commit() 
 conn.close()
 
def on_message_ack(client, userdata, message):
    #print("received message: " ,str(message.payload.decode("utf-8")))
    global ackn,msg
    ackn=1
    msg=str(message.payload.decode("utf-8"))
def sql_data(s):
    s="'"+s+"'"
    return s
def sql_datasend(room_new,device_new,appliance1_new,appliance2_new,appliance3_new,appliance4_new):
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
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
def on_message(client, userdata, message):
    global i,msg
    i=1
    msg=str(message.payload.decode("utf-8"))

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
 if APPLIANCE_NEW=="All":
     cur.execute("SELECT * FROM CONTROLBOX_CONFIG")
     for room,device,appliance1,appliance2,appliance3,appliance4 in cur:
         
        print(room,device,appliance1,appliance2,appliance3,appliance4 )
        #global user_dt,password_dt
        conn1 = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 
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
 #print(status)
 return status
hist=0
msg_hist=""
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
 d1 = datetime.datetime(int(str(fromdate[6])+str(fromdate[7])+str(fromdate[8])+str(fromdate[9])),int(str(fromdate[3])+str(fromdate[4])),int(str(fromdate[0])+str(fromdate[1])))
 d2 = datetime.datetime(int(str(todate[6])+str(todate[7])+str(todate[8])+str(todate[9])),int(str(todate[3])+str(todate[4])),int(str(todate[0])+str(todate[1])))
 cur.execute("SELECT * FROM "+table_name+" WHERE APPLIANCE="+sql_data(appliance)+"AND LOCATION="+sql_data(location))
 for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur:

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
     
     
     
     
def on_message_live(client, userdata, message):
    global live,msg_live
    live=1
    msg_live=str(message.payload.decode("utf-8"))    
    print("received message: " ,msg_live)

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")    




conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
cur = conn.cursor()
contacts = []

dump=1
cur.execute("select * from GATEWAY_CONFIG")
for ssid,password,ip_address in cur:
     dump=0
if dump==0:
 mqttBroker =ip_address
 user = "username" 
 password = "password"
 client = mqtt.Client("subscriber")
 client.message_callback_add('ack/#', on_message_ack)
 client.message_callback_add('configure/#', on_message)
 client.message_callback_add("livestatus/#",on_message_live )
 client.message_callback_add("history/sub",on_message_history )
 client.username_pw_set(user, password=password)    #set username and password
 client.on_connect= on_connect                  
 client.connect(mqttBroker,1884) 
 client.loop_start()
 client.subscribe("configure/#")
 client.subscribe("ack/#")
 client.subscribe("livestatus/#")
 client.publish("live/pub","mainprog")
 client.publish("history/pub","mainprog")
 client.subscribe("history/sub")
 
 print("hello")
 while True:
   if i==1:
        print(msg)
        i=0
        dict_obj = json.loads(msg)
        print(dict_obj.get('Room'),dict_obj.get('Device'),dict_obj.get('Appliance1'),dict_obj.get('Appliance2'),dict_obj.get('Appliance3'),dict_obj.get('Appliance4'))
        sql_datasend(dict_obj.get('Room'),dict_obj.get('Device'),dict_obj.get('Appliance1'),dict_obj.get('Appliance2'),dict_obj.get('Appliance3'),dict_obj.get('Appliance4'))
        msg=' '
   if ackn==1:
      print(msg)
      ackn=0
      dict_obj = json.loads(msg)
      STATE="0"
      if dict_obj.get('state')!="0":
        STATE="1"
      msg=' '
      sql_datasend_ack(dict_obj.get('Location'),dict_obj.get('Username'),dict_obj.get('Appliance'),STATE)
   if live==1:
     live=0
     live=0
     print(msg_live)
     dict_obj = json.loads(msg_live)
     username=str(dict_obj.get("Username"))
     accesskey=str(dict_obj.get("AccessKey"))
     sent=sql_datasend_livestatus(dict_obj.get("location"),dict_obj.get("appliance"))
     sent='{"Username":"'+username+'" ,"AccessKey":"'+accesskey+'","status":'+sent+'}'
     print(sent)
     client.publish("live/pub",sent)
     
     
     
     
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




