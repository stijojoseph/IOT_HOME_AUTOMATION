import paho.mqtt.client as mqttClient
import time
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
# Enter ip address of pi and also username and password used for local broker. 
broker_address= "192.168.43.81"
port = 1884
user = "username"
password = "password"
 
client = mqttClient.Client("ESP8266client")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
        #write the condition to execute in loop. below condition ON and OFF plug 1 in every 2 sec.
        print("Turning ON the Appliance")
        client.publish("Room_name/device_name",'{"Aplliance":"14", "state":"ON"}')
        time.sleep(2) #Delay 2 sec.
        print("Turning OFF the Appliance")
        client.publish("Room_name/device_name",'{"Aplliance":"14", "state":"OFF"}')
        
        time.sleep(2) #Delay 2 sec.
        
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()

