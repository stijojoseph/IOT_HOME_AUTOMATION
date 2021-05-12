import mariadb
import json
import sys 
import time
from datetime import datetime
# Connect to MariaDB Platform
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
    
def sql_data(s):
    s="'"+s+"'"
    return s
def sql_datasend(LOCATION_NEW,CLIENT_NEW,APPLIANCE_NEW,STATE):
 insert="1"
 update="0"
 now = datetime.now()
 #getting the current time
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
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []
 table_name="ROOM_CONTROLBOX_APPLIANCE"
 dump=1
 cur.execute("select * from "+table_name)
 #checking the control box configuration table 
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
 
data='{"Username":"username","AccessKey":"xyz","Location":"Lobby","Appliance":"Light1","state":"0"}'

dict_obj = json.loads(data)
STATE="0"
if dict_obj.get('state')!="0":
    STATE="1"

sql_datasend(dict_obj.get('Location'),dict_obj.get('Username'),dict_obj.get('Appliance'),STATE)
