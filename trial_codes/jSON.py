import json
import mariadb
import datetime
def sql_data(s):
    s="'"+s+"'"
    return s


def data_give(location,appliance,fromdate,todate):
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 json_data= ""
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
 json_data="[ "+json_data+" ]"   
 return json_data
loc="Lobby"
app="light3"
fromd="30/04/2021"
tod="02/05/2021"
print(data_give(loc,app,fromd,tod))