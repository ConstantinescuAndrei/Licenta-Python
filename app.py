from flask import Flask, request
import datetime
import json
import pyrebase

# db.child("temperature_sensor").child("Joe").set(data)

config = {
    "apiKey": "AIzaSyDY2ynYDDC5LMRhqZaM9x5xjDwryDAwJII",
    "authDomain": "monitoringanimalparametersapi.firebaseapp.com",
    "databaseURL": "https://monitoringanimalparametersapi.firebaseio.com",
    "projectId": "monitoringanimalparametersapi",
    "storageBucket": "monitoringanimalparametersapi.appspot.com",
    "messagingSenderId": "1042253543113",
    "appId": "1:1042253543113:web:79dd8f9a6f5013aef87f18",
    "measurementId": "G-VQRT3VD9BY"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# print('Do you wanna sign in?')

# answer = input('Y/N\n')

# if answer == 'Y':
#     email = input('Email:')
#     print('\n')
#     password = input('Password:')
#     print('\n')
#     user = auth.sign_in_with_email_and_password(email, password)
#     auth.send_email_verification(user['idToken'])
#     print(json.dumps(auth.get_account_info(user['idToken']), sort_keys=True, indent=4))

# print('Do you wanna log in?')

# answer = input('Y/N\n')

# if answer == 'Y':
#     email = input('Email:')
#     print('\n')
#     password = input('Password:')
#     print('\n')
#     user = auth.create_user_with_email_and_password(email, password)
#     print(json.dumps(auth.get_account_info(user['idToken']), sort_keys=True, indent=4))

# user = auth.create_user_with_email_and_password(email, password)
db = firebase.database()

app = Flask(__name__)

def jprint(obj):
    # create a formatted string of the Python JSON object
    jSON = json.dumps(obj, sort_keys=True, indent=4)
    return jSON

# response = requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon;=-74")
# print(response.status_code)
# jprint(response.json())

def addToDBTempSensor(data):
    db.child("temperature_sensor").push(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username)
    print(password)
    return '<h1>Hello</h1>'

@app.route('/temperature', methods=['GET', 'POST'])
def getTemperature():
    data = {}    
    now = datetime.datetime.now()
    temperature = request.args.get('temperature')   
    umidity = request.args.get('umidity')
    account = request.args.get('account')
    data['temperature'] = temperature
    data['umidity'] = umidity
    data['account'] = account
    data['year'] = now.year
    data['month'] = now.month
    data['day'] = now.day
    data['hour'] = now.hour
    data['minute'] = now.minute
    addToDBTempSensor(data)
    return '<h1>It worked</h1>'

@app.route('/')
def main():
    return 'Hello'

@app.route('/getById/<id>', methods=['GET'])
def getById(id):
    print(id)
    data = db.child("temperature_sensor").get()
    data = jprint(data.val())
    print(data(3))
    return 'HELLOOOOO'

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username)
    print(password)
    return "Account created"

if __name__ == '__main__':
    app.run()