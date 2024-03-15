
from flask import Flask, render_template, request
import joblib
import numpy as np
import urllib.request
import urllib.parse
import os
from twilio.rest import Client

app = Flask(__name__)
model = joblib.load('model.sav')
# Twilio account credentials
account_sid = "ACad2ca85a96cf98c15a63af88b13ec0c9"
auth_token = "42a9784482df2adbf3eccbdf6654ef41"
twilio_phone_number = "+13027516269"  # Your Twilio phone number
verified_recipient_number = "+919553495889"  # Your verified recipient number

# Initialize Twilio client
client = Client(account_sid, auth_token)



def send_sms(data):
    account_sid = "AC48b8442ca1a1bdfb07a788e334e53412"
    auth_token = "c1f8caf3ec0ff44602197862454e65e2"
    client = Client(account_sid, auth_token)

    from_number = "+13027516269"  # Your Twilio phone number
    verified_number = "+919553495889"
    message_body=data

    try:
        message = client.messages.create(body=message_body, from_="+13027516269", to="+919553495889")
        print("Message sent successfully! SID")
    except Exception as e:
        print("Failed to send message:", str(e))

def cal(ip):
    input_data = dict(ip)
    Did_Police_Officer_Attend = input_data['Did_Police_Officer_Attend'][0]
    age_of_driver = input_data['age_of_driver'][0]
    vehicle_type = input_data['vehicle_type'][0]
    age_of_vehicle = input_data['age_of_vehicle'][0]
    engine_cc = input_data['engine_cc'][0]
    day = input_data['day'][0]
    weather = input_data['weather'][0]
    light = input_data['light'][0]
    roadsc = input_data['roadsc'][0]
    gender = input_data['gender'][0]
    speedl = input_data['speedl'][0]

    data = np.array(
        [Did_Police_Officer_Attend, age_of_driver, vehicle_type, age_of_vehicle, engine_cc, day, weather, roadsc, light,
         gender, speedl])

    print("logging", data)
    data = data.astype(float)
    data = data.reshape(1, -1)

    x = np.array([1, 3.73, 3, 0.69, 125, 4, 1, 1, 1, 1, 30]).reshape(1, -1)

    try:
        result = model.predict(data)
        # Convert result to integer
        result_int = int(result[0])
        return str(result_int)
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/map', methods=['GET'])
def map():
    return render_template('map.html')

@app.route('/', methods=['POST'])
def get():
    a= cal(request.form)
    if a==1:
        send_sms("Your Accident Severity Prediction was 'Fatal'. ")
    elif a==2:
        send_sms("Your Accident Severity Prediction was 'Serious'. ")
    else:
        send_sms("Your Accident Severity Prediction was 'Slight'. ") 
    return a

if __name__ == '__main__':
    app.run(debug=True)

