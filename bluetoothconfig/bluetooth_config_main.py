from bluetooth import *
import mariadb
from re import search
import sys 
import time
import json
#bluetooth socket starting
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1000)

port = server_sock.getsockname()[1]

user_dt="root"
password_dt="password"


user_id=' '
password=' '
securitykey=' '
print("Waiting for connection on RFCOMM channel %d" % port)
print("###################################################\n")
print("Again Waiting for connection on RFCOMM channel %d go to another serial monitor bluetooth app and connect again from mobile" % port)
print("\n Enter MSG(json format) as per the given format in document ")
print("###################################################\n")
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
def sql_data(s):
    s="'"+str(s)+"'"
    return s
    
    
def sql_datasend(userid,password,securitykey):
 #connecting to the database   
 global user_dt,password_dt
 conn = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 dump=1
 
 
 use=''
 c={",","(",")","'"}
 use=""
 cur.execute("select USER_ID from USERS_DATA ")
 for k in cur:
    for t in k:
       if t not in c:
           use+=t
    
    print(use)    
    if userid==use:
     #if the userid already exist intable update his password and security
     dump=0
     
     conn1 = mariadb.connect( user=user_dt, password=password_dt, host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
     print("current user updated")
     cur1 = conn1.cursor()
     cur1.execute("UPDATE USERS_DATA SET PASSWORD="+sql_data(password)+",SECURITY_KEY="+sql_data(securitykey)+" where USER_ID="+sql_data(userid))
     conn1.commit()
    use='' 
    #print(k,dat,sk)"""
 if dump==1:
  #if username not found in database add the new user dateails to database   
  print("new user added \n")   
  dump=0
  cur.execute("INSERT INTO USERS_DATA(USER_ID,PASSWORD,SECURITY_KEY) VALUES (?,?,?)",(userid,password,securitykey))
  conn.commit()

#conn.commit() 
 conn.close()


    
    
def check(msg):
#msg format
#{ “userid” : “your_username” , “password” : “your_password” , “securitykey” :
#“secure”, “command” : “wificonfig”}


    dict_obj = json.loads(msg)
    print(msg)
    #extraction of parameter from json structure
    userid1=dict_obj.get('userid')
    password1=dict_obj.get('password')
    securitykey1=dict_obj.get('securitykey')
    status1=dict_obj.get('command')
    #username,password,securitykey send to database for storage
    sql_datasend(userid1,password1,securitykey1)
    #checking wheather to switch to wifi configuration mode
    if status1=="wificonfig":
        client_sock.close()
        server_sock.close()
        cmd = 'sudo python3 run_main.py'
        cmd_result = os.system(cmd)
  
    
    
    

while True:
    #IF ANY DATA RECIEVED FROM CHANNEL, WILL BE STORED data variable
        data = client_sock.recv(1024)
        
        if len(data) != 0:
          
         #print("received \n",data)
         check(str(data.decode('utf-8')))

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
