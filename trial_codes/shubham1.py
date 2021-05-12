import paho.mqtt.client as mqttClient
import time
import json
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
# Enter ip address of pi and also username and password used for local broker. 
broker_address= "broker.mqttdashboard.com"
port = 1883
#user = "testingdevice1"
#password = "testingdevice1"
 
client = mqttClient.Client("pyclient")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)

now = time.strftime('%H:%M:%S')

#x =  {"now":now, "name":"Shubham"}
#msg = json.dumps(x)

try:
    while True:
        #write the condition to execute in loop. below condition ON and OFF plug 1 in every 2 sec.
        print("Sending msg")
        client.publish("IoTAssignment_Shubham","hello")    #("Topic", "message")
        time.sleep(2) #Delay 2 sec.

        
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()
