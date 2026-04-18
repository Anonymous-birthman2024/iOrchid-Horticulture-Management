from flask import Flask
username = "Lucy"
app = Flask(__name__)

index = open("index.html", "r")

@app.route("/")
def hello_world():
    return index.read()
    

@app.route("/program")
def program():
    return '''
    <p> Write program here </p>
    '''