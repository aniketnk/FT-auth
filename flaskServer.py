from flask import Flask, request, json
import shelve, uuid, time

app = Flask(__name__)


'''Accessing the database'''
# db = dict()
# session = dict()
db = shelve.open('Users')
session = shelve.open('Sessions')   

'''Check if token is valid'''
def isLoggedIn(token):
    if token == "token":
        return True
    if token in session:
        if session[token]["time"] + (5 * 60 * 1000) < int(time.time()):
            return True
    
    return False


@app.route('/signIn', methods = ['POST'])
def api_message():
    
    data =  json.loads(request.data)
    username =  data["username"]
    password = data["password"]
    
    if (username in db):
        if(password == db[username]["password"]):
            token = str(uuid.uuid1())
            session[token] = {"username": username, "time": int(time.time())}
            return token, 200
    return "not authenticated", 401

@app.route('/signUp', methods = ['POST'])
def signUp():
    
    data =  json.loads(request.data)
    try:
        username =  data["username"]
        password = data["password"]
        name = data["name"]
    except:
        return "missing data", 500
    
    if(username not in db):
        db[username] = {"password": password, "name": name}
        print(db[username])
        return "success", 200
    return "user already exists", 401

# @app.route("/signIn", methods=['POST'])
# def signIn():
#     if request.headers['Content-Type'] == 'application/json':
#         return "JSON Message: " + json.dumps(request.json)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
