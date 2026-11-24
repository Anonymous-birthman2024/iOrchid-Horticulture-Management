from pathlib import Path
from flask import Flask, abort

BASE_DIR = Path(__file__).resolve().parent
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
