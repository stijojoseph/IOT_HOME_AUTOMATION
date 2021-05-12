import mariadb

import sys 
import time
from datetime import datetime
# Connect to MariaDB Platform

def sql_datasend():
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 userid="admin2"
 dump=1
 cur.execute("select * from USERS_DATA")
 for k,dat,sk in cur:
    for char in k:
     if char in " ?.!/;:":
        k.replace(char,'')
    if k==userid:
     dump=0
    print(k,dat,sk)
 if dump==1:
  print("new user added \n")   
  password="adminpassword"
  securitykey="adminsecurity"
  cur.execute("INSERT INTO USERS_DATA(USER_ID,PASSWORD,SECURITY_KEY) VALUES (?,?,?)",(userid,password,securitykey))
  conn.commit()

#conn.commit() 
 conn.close()
sql_datasend()