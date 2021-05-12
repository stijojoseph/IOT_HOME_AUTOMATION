import json

loc="lobby"
app="light1"
user="username1"
on="22:04:34"
off="23:05:34"
total="0 HRS 34 MINS"
json1='{"LOCATION":"'+loc+'","APPLIANCE":"'+app+'","USERNAME":"'+user+'","ON_TIME":"'+on+'","OFF_TIME":"'+off+'","TOTAL_ON_TIME":"'+total+'"}'
sr=json.loads(json1)
js=json.dumps(sr)
js=js+","+js
print(js)