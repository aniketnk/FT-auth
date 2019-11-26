#!/usr/bin/env python3

from flask import Flask, request, json
import shelve
import uuid
import time
import math
import random
import smtplib

app = Flask(__name__)


'''Accessing the database'''
db = dict()
session = dict()
validatedSession = dict()
# db = shelve.open('UsersDB')
# session = shelve.open('SessionsDB')

'''Check if token is valid'''


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def isLoggedIn(token):
    if token == "token":
        return True
    if token in session:
        if session[token]["time"] + (5 * 60 * 1000) < int(time.time()):
            return True

    return False


def sendEmail(username, email, otp):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("rr8049879@gmail.com", "<enter password here>")
    message = "Hi " + username + ", " + "here's the OTP you can use to login. " + otp
    body = 'Subject: {}\n\n{}'.format("OTP For Login", message)
    s.sendmail("rr8049879@gmail.com", email, body)
    s.quit()


@app.route('/signIn', methods=['POST'])
def api_message():
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]
    email = data["email"]

    if (username in db):
        if(password == db[username]["password"]):
            token = str(uuid.uuid1())
            otp = str(generateOTP())
            tokenOtpPair = token+","+otp
            sendEmail(username, email, otp)
            validatedSession[tokenOtpPair] = {"username": username}
            session[token] = {"username": username, "time": int(time.time())}
            return token, 200
    return "not authenticated", 401


@app.route('/signUp', methods=['POST'])
def signUp():

    data = json.loads(request.data)
    try:
        username = data["username"]
        # email = data["email"]
        email = "rishiravi.k98@gmail.com"

        password = data["password"]
        name = data["name"]
    except:
        return "missing data", 500

    if(username not in db):
        db[username] = {"email": email, "password": password, "name": name}
        print(db[username])
        return "success", 200
    return "user already exists", 401

# @app.route("/signIn", methods=['POST'])
# def signIn():
#     if request.headers['Content-Type'] == 'application/json':
#         return "JSON Message: " + json.dumps(request.json)


@app.route("/verifyOtp", methods=["POST"])
def verifyOtp():
    data = json.loads(request.data)
    otp = data["otp"]
    token = data["token"]
    username = data["username"]

    key = token+","+otp
    print(validatedSession[key])
    if ((username in db) and (key in validatedSession)):
        if(username == validatedSession[key]["username"]):
            return token, 200
    return "not authenticated", 401


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    # portNum = int(input("Communication port: ") or 5000)
    app.run(port=5000, debug=False)
