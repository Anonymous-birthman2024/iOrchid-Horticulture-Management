from pathlib import Path
from flask import Flask, abort, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
username = "Lucy"
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")

def read_text(path: str) -> str:
    target = (BASE_DIR / path).resolve()
    if BASE_DIR not in target.parents:
        abort(404)
    try:
        return target.read_text(encoding="utf-8")
    except FileNotFoundError:
        abort(404)

@app.route("/")
def home():
    return read_text("index.html").replace("{username}", username)

@app.route("/program")
def program():
    return read_text("iOrchid-Horticultural-Frontend.html")

@app.route("/z<int:zone>")
def zone_page(zone):
    if not 1 <= zone <= 6:
        abort(404)
    return read_text(f"zone{zone}.html")

@app.route("/graphs/<zone>/<sensor>/<filename>")
def graph(zone, sensor, filename):
    if zone not in {f"Zone{i}" for i in range(1, 7)}:
        abort(404)
    if sensor not in {"hum", "light", "temp"} or filename not in {"graph.png", "graph2.png"}:
        abort(404)
    directory = PROJECT_DIR / zone / "data_DO_NOT_MODIFY" / "graphs" / sensor
    return send_from_directory(directory, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
