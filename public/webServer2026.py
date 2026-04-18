from flask import Flask
username = "Lucy"
app = Flask(__name__)

#each file is a web page.
index = open("./index.html", "r")
programApp = open("iOrchid-Horticultural-Frontend.html", "r")

@app.route("/")
def hello_world():
    return index.read().replace("{username}", username)
    

@app.route("/program")
def program():
    return programApp.read()

@app.route("/z1")
def zone1():
    return "Content for Zone 1"

@app.route("/z2")
def zone2():
    return "Content for Zone 2"

@app.route("/z3")
def zone3():
    return "Content for Zone 3"

@app.route("/z4")
def zone4():
    return "Content for Zone 4"

@app.route("/z5")
def zone5():
    return "Content for Zone 5"

@app.route("/z6")
def zone6():
    return "Content for Zone 6"

