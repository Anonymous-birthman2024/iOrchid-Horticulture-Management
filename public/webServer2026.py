from flask import Flask

'''
IMPORTANT CONNECTION INFORMATION:

ALWAYS HOST ON 192.168.1.81, PORT 5002!!!!!!!!!!


'''

express_port_change = ["localhost", '5002'] #Changing this will change the port that the web server is hosted on. Do not mess with this!
username = "Lucy"
app = Flask(__name__)

# each file is a web page
index = open("index.html", "r")
programApp = open("iOrchid-Horticultural-Frontend.html", "r")
z1 = open("zone1.html", "r")
z2 = open("zone2.html", "r")
z3 = open("zone3.html", "r")
z4 = open("zone4.html", "r")
z5 = open("zone5.html", "r")
z6 = open("zone6.html", "r")

@app.route("/")
def home():
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


if __name__ == "__main__":
    app.run(host=f"{express_port_change[0]}", port=int(express_port_change[1]), debug=True)