from flask import Flask
import request
app = Flask(__name__)

@app.route('/hello')
def index():
    
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=False,host="192.168.43.81")