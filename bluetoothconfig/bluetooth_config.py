from bluetooth import *
import json
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1000)

port = server_sock.getsockname()[1]
print("###################################################\n")
print("Again Waiting for connection on RFCOMM channel %d go to another serial monitor bluetooth app and connect again from mobile" % port)
print("\n Enter the userid,password,securitykey one by one as per the given format or type 'restart' to switch wifi configuration settings ")
print("###################################################\n")
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
def check(stri):
    if "userid" in stri:
        store(stri,"userid")
    if "password" in stri:
        store(stri,"password")
    if "securitykey" in stri:
        store(stri,"securitykey")  
def store(test,user):
 
 userid=''
 if user in test:
    for i in range(len(user)+1,len(test)):
        userid+=test[i]
 print(userid)

while True:
        data = client_sock.recv(1024)
        if len(data) != 0:
          
         print("received \n",data)
         check(data)

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")