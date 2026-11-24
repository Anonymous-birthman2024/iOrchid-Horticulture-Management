"""Generate current sensor snapshots as PNG charts.

Historical sampling belongs in the monitoring process; graph generation must
never block application startup for weeks.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

def _plot(zone, sensor, filename, title, unit):
    data_dir = ROOT / zone / "data_DO_NOT_MODIFY"
    value = float((data_dir / f"{sensor}_data.txt").read_text(encoding="utf-8").strip())
    output_dir = data_dir / "graphs" / sensor
    output_dir.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots()
    axis.plot([0], [value], marker="o")
    axis.set(title=f"{zone} {title}", xlabel="Latest reading", ylabel=unit)
    axis.grid(True)
    figure.tight_layout()
    figure.savefig(output_dir / filename)
    plt.close(figure)

def humeGrapherWeek(zone): _plot(zone, "hum", "graph.png", "Weekly Humidity", "%")
def humeGrapherMonth(zone): _plot(zone, "hum", "graph2.png", "Monthly Humidity", "%")
def lightGrapherWeek(zone): _plot(zone, "light", "graph.png", "Weekly Light", "lux")
def lightGrapherMonth(zone): _plot(zone, "light", "graph2.png", "Monthly Light", "lux")
def tempGrapherWeek(zone): _plot(zone, "temp", "graph.png", "Weekly Temperature", "°C")
def tempGrapherMonth(zone): _plot(zone, "temp", "graph2.png", "Monthly Temperature", "°C")
