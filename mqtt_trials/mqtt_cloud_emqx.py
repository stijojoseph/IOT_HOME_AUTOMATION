import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {rc}")
   

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
def on_message1(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))    
client = mqtt.Client()
client.on_connect = on_connect



# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)
client.subscribe("Room_name/room1")
client.on_message=on_message1
# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
