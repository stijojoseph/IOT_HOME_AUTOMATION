import json
import mariadb
def sql_data(s):
    s="'"+s+"'"
    return s

appliance="Light3"
location="Lobby"
table_name="ROOM_CONTROLBOX_APPLIANCE"
print(json.dumps((location,appliance)))
conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
cur = conn.cursor()
cur.execute("SELECT * FROM "+table_name+" WHERE APPLIANCE="+sql_data(appliance)+"AND LOCATION="+sql_data(location))
for DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME in cur:
    print(DATE,LOCATION,CLIENT,APPLIANCE,ON_TIME,OFF_TIME,TOTAL_ON_TIME)