import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print"Connected with result code "
   
 
# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print"hei"
def on_message1(client, userdata, message):
    print"received message: " ,str(message.payload.decode("utf-8"))    
client = mqtt.Client("raspberrypi")
client.on_connect = on_connect



# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("node02.myqtthub.com", 1883, 60)
client.subscribe("stijo")
client.on_message=on_message1
# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
