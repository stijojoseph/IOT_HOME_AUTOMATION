import time
import mariadb

import sys 
import time
from datetime import datetime
i=0;
def sql_data(s):
    s="'"+s+"'"
    return s
def sql_datasend(LOCATION_NEW,APPLIANCE_NEW):
 status="OFF"   
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 table_name="ROOM_CONTROLBOX_APPLIANCE"
 dump=1
 cur.execute("select * from "+table_name+" where LOCATION="+sql_data(LOCATION_NEW)+"and APPLIANCE="+sql_data(APPLIANCE_NEW)+"and OFF_TIME="+sql_data("NULL"))
 for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur: 
   status="ON"
   print(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME)     
 return status
 
 
 
print(sql_datasend("Lobby","Light2"))     
     
