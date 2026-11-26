from pathlib import Path
import sys
import threading

from flask import Flask, abort, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from modules_DO_NOT_MODIFY import grapher
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

_graph_locks = {}
_graph_locks_guard = threading.Lock()

_GRAPH_BUILDERS = {
    ("hume", "graph.png"): grapher.humeGrapherWeek,
    ("hume", "graph2.png"): grapher.humeGrapherMonth,
    ("light", "graph.png"): grapher.lightGrapherWeek,
    ("light", "graph2.png"): grapher.lightGrapherMonth,
    ("temp", "graph.png"): grapher.tempGrapherWeek,
    ("temp", "graph2.png"): grapher.tempGrapherMonth,
}


@app.route("/graphs/<zone>/<sensor>/<filename>")
def graph(zone, sensor, filename):
    if zone not in {f"Zone{i}" for i in range(1, 7)}:
        abort(404)
    builder = _GRAPH_BUILDERS.get((sensor, filename))
    if builder is None:
        abort(404)

    directory = PROJECT_DIR / zone / "data_DO_NOT_MODIFY" / "graphs" / sensor
    image_path = directory / filename

    # Generate the requested image on demand. This makes the page resilient
    # if startup graph generation was skipped or an image was deleted.
    if not image_path.is_file() or image_path.stat().st_size == 0:
        with _graph_locks_guard:
            lock = _graph_locks.setdefault((zone, sensor, filename), threading.Lock())
        with lock:
            if not image_path.is_file() or image_path.stat().st_size == 0:
                try:
                    builder(zone)
                except Exception:
                    app.logger.exception(
                        "Could not generate %s graph for %s", sensor, zone
                    )
                    abort(500)

    if not image_path.is_file() or image_path.stat().st_size == 0:
        app.logger.error("Graph image was not created: %s", image_path)
        abort(404)

    response = send_from_directory(directory, filename, mimetype="image/png")
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
