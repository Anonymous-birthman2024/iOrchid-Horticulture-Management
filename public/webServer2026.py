from pathlib import Path
from flask import Flask

'''
IMPORTANT CONNECTION INFORMATION:

ALWAYS HOST ON 192.168.1.71, PORT 5002!!!!!!!!!!


'''

BASE_DIR = Path(__file__).resolve().parent
express_port_change = ["localhost", '5002'] #Changing this will change the port that the web server is hosted on. Do not mess with this!
username = "Lucy"
app = Flask(__name__, static_folder='.', static_url_path='')


def read_text(path: str) -> str:
    return (BASE_DIR / path).read_text(encoding="utf-8")


@app.route("/")
def home():
    return read_text("index.html").replace("{username}", username)


@app.route("/program")
def program():
    return read_text("iOrchid-Horticultural-Frontend.html")


@app.route("/z1")
def zone1():
    return read_text("zone1.html")


@app.route("/z2")
def zone2():
    return read_text("zone2.html")


@app.route("/z3")
def zone3():
    return read_text("zone3.html")


@app.route("/z4")
def zone4():
    return read_text("zone4.html")


@app.route("/z5")
def zone5():
    return read_text("zone5.html")


@app.route("/z6")
def zone6():
    return read_text("zone6.html")


if __name__ == "__main__":
    app.run(host=f"{express_port_change[0]}", port=int(express_port_change[1]), debug=True)