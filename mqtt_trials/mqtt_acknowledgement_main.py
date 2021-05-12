import paho.mqtt.client as mqtt
import time
i=0;
def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")    
    
user = "username"
password = "password"    
mqttBroker ="192.168.43.81"

client = mqtt.Client("subscriber")
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                  
client.connect(mqttBroker,1884) 

client.loop_start()

client.subscribe("status/#")
client.on_message=on_message 
print("hello")
time.sleep(20000)
client.loop_stop()



