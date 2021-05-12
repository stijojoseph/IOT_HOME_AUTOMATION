from flask import Flask
from flask import jsonify,request
no=0
app = Flask(__name__)

courses=[{"courses":"science"},{"classes":"maths"}]    
         

@app.route('/')
def index():
    return 'REST API STARTED STUDYING'

@app.route('/check')
def cakes():
    global no
    if 'no' in request.args:
        no=int(request.args['no'])
    print(no)   
    return str(courses[no])

@app.route('/page2')
def cakes2():
    return 'next page2'

@app.route("/courses",methods={'GET'})
def get():
    return jsonify({"course":courses})



if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.81')