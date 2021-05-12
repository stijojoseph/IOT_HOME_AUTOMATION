import paho.mqtt.client as mqtt
import time
import mariadb
from datetime import datetime
import sys 
b=" "

# Connect to MariaDB Platform

conn = mariadb.connect( user="root", password="raspberry", host="localhost",port=3306,database="MQTT_DATABASE1" )

def on_message_data1(client, userdata, message):
      print("received message: " ,str(message.payload.decode("utf-8")))
      b=str(message.payload.decode("utf-8"))
      now = datetime.now()
      dt= now.strftime("%d/%m/%Y");
      tm=now.strftime("%H:%M:%S")
      cur = conn.cursor()
      cur.execute("INSERT INTO MQTT_DATA_1(DATA,TIME,DATE) VALUES (?,?,?)",
      (b,dt,tm))
      conn.commit()
      print("\n publshed")
def on_message_data3(client, userdata, message):
      print("received message: " ,str(message.payload.decode("utf-8")))
      b=str(message.payload.decode("utf-8"))
      now = datetime.now()
      cur = conn.cursor()
      dt= now.strftime("%d/%m/%Y");
      tm=now.strftime("%H:%M:%S")
      cur = conn.cursor()
      cur.execute("INSERT INTO MQTT_DATA_2(DATA,TIME,DATE) VALUES (?,?,?)",
      (b,dt,tm))
      conn.commit()
      print("\n publshed")

def on_message_data4(client, userdata, message):
      print("received message: " ,str(message.payload.decode("utf-8")))
      b=str(message.payload.decode("utf-8"))
      now = datetime.now()
      cur = conn.cursor()
      dt= now.strftime("%d/%m/%Y");
      tm=now.strftime("%H:%M:%S")
      cur = conn.cursor()
      cur.execute("INSERT INTO MQTT_DATA_3(DATA,TIME,DATE) VALUES (?,?,?)",
      (b,dt,tm))
      conn.commit()
      print("\n publshed")
def on_message_data2(client, userdata, message):
      print("received message: " ,str(message.payload.decode("utf-8")))
      b=str(message.payload.decode("utf-8"))
      now = datetime.now()
      cur = conn.cursor()
      dt= now.strftime("%d/%m/%Y");
      tm=now.strftime("%H:%M:%S")
      cur = conn.cursor()
      cur.execute("INSERT INTO MQTT_DATA_4(DATA,TIME,DATE) VALUES (?,?,?)",
      (b,dt,tm))
      conn.commit()
      print("\n publshed")

      

mqttBroker ="192.168.43.81"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("data1")
client.subscribe("data2")
client.subscribe("data3")
client.subscribe("data4")


client.message_callback_add('data1',on_message_data1)
client.message_callback_add('data2',on_message_data2)
client.message_callback_add('data3',on_message_data3)
client.message_callback_add('data4',on_message_data4)


time.sleep(60)
client.loop_stop()
