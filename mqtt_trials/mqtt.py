import paho.mqtt.client as mqtt
import time
i=0;
def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    
    
mqttBroker ="192.168.43.81"

client = mqtt.Client("subscriber")
client.connect(mqttBroker,1883) 

client.loop_start()

client.subscribe("Room_name/room1")
client.on_message=on_message 
print("hello")
time.sleep(2000)
client.loop_stop()