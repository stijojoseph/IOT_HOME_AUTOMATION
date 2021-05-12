# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
import json
import mariadb
import datetime
def sql_data(s):
    s="'"+s+"'"
    return s

# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.


# returns the data that we send when we use POST.
@app.route("/json", methods=['GET', 'POST'])
def starting_url():
    json_data = request.json
    location= str(json_data["Location"])
    appliance=str(json_data["Appliance"])
    from_date=str(json_data["from_date"])
    to_date=str(json_data["to_date"])
    return data_give(location,appliance,from_date,to_date)

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
 json_data=json.loads(json_data)
 json_data=json.dumps(json_data)
 print(json_data)
 return json_data
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<string:location>/<string:appliance>/<string:from_date>/<string:to_date>', methods = ['GET'])
def disp(location,appliance,from_date,to_date):
    #print(location,appliance,from_date,to_date)
	return location+" "+ appliance+" "+from_date+" "+to_date


# driver function
if __name__ == '__main__':

	app.run(debug =False,host="192.168.43.81",port= 8090)
