import mariadb

def sql_datasend():
 conn = mariadb.connect( user="root", password="password", host="localhost",port=3306,database="SQL_GATEWAY_DATABASE")
 cur = conn.cursor()
 contacts = []

 dump=1
 cur.execute("select * from GATEWAY_CONFIG")
 for ssid,password,ip_address in cur:
     dump=0
 if dump==0:
     print(ip_address)
     
sql_datasend()     