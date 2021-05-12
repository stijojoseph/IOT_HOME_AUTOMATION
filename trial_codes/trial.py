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

check("userid:stijojoseph")
check("password:password1")
check("securitykey:abcd")