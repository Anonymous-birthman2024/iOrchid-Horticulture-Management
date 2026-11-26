"""Create weekly and monthly graphs from saved sensor history.

Each sensor monitor appends one timestamped reading every five minutes.
Graph generation only reads the history already collected; it does not wait
for a week or a month during application startup.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Safe for Flask/server environments without a display.
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import threading
import time

from modules_DO_NOT_MODIFY.sensor_storage import (
    read_history,
    read_integer,
    zone_data_dir,
)

SENSOR_INFO = {
    "hume": {
        "label": "Humidity",
        "unit": "%",
        "current_file": "hum_data.txt",
        "folder": "hume",
    },
    "light": {
        "label": "Light intensity",
        "unit": "lux",
        "current_file": "light_data.txt",
        "folder": "light",
    },
    "temp": {
        "label": "Temperature",
        "unit": "°C",
        "current_file": "temp_data.txt",
        "folder": "temp",
    },
}


def _graph_sensor(zone, sensor, days, output_name):
    if sensor not in SENSOR_INFO:
        raise ValueError(f"Unknown sensor: {sensor}")

    info = SENSOR_INFO[sensor]
    samples = read_history(zone, sensor)

    # If history has not been created yet, show the current reading as a
    # single point rather than failing or inventing historical measurements.
    if not samples:
        current_value = read_integer(zone_data_dir(zone) / info["current_file"])
        if current_value is not None:
            samples = [(datetime.now(timezone.utc), current_value)]

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    normalized_samples = []
    for timestamp, value in samples:
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)

        if timestamp >= cutoff:
            normalized_samples.append((timestamp, value))

    normalized_samples.sort(key=lambda item: item[0])

    output_dir = zone_data_dir(zone) / "graphs" / info["folder"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_name

    fig, ax = plt.subplots(figsize=(12, 5))
    try:
        if normalized_samples:
            timestamps = [item[0] for item in normalized_samples]
            values = [item[1] for item in normalized_samples]
            ax.plot(timestamps, values, linewidth=1.4)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))
            fig.autofmt_xdate()
        else:
            ax.text(
                0.5,
                0.5,
                "No sensor readings available yet",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

        ax.set_title(f"{info['label']} — {zone} (last {days} days)")
        ax.set_xlabel("Date and time (UTC)")
        ax.set_ylabel(info["unit"])
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(output_path, dpi=150)
    finally:
        plt.close(fig)

    return str(output_path)


def humeGrapherWeek(zone):
    return _graph_sensor(zone, "hume", 7, "graph.png")


def humeGrapherMonth(zone):
    return _graph_sensor(zone, "hume", 30, "graph2.png")


def lightGrapherWeek(zone):
    return _graph_sensor(zone, "light", 7, "graph.png")


def lightGrapherMonth(zone):
    return _graph_sensor(zone, "light", 30, "graph2.png")


def tempGrapherWeek(zone):
    return _graph_sensor(zone, "temp", 7, "graph.png")


def tempGrapherMonth(zone):
    return _graph_sensor(zone, "temp", 30, "graph2.png")



_refresh_threads = {}
_refresh_lock = threading.Lock()


def refresh_zone_graphs(zone):
    """Regenerate all six graph images for one zone."""
    humeGrapherWeek(zone)
    humeGrapherMonth(zone)
    lightGrapherWeek(zone)
    lightGrapherMonth(zone)
    tempGrapherWeek(zone)
    tempGrapherMonth(zone)


def start_graph_refresh(zone, interval=300):
    """Refresh a zone's graphs periodically without blocking application startup."""
    if interval <= 0:
        raise ValueError("Graph refresh interval must be greater than zero.")

    with _refresh_lock:
        thread = _refresh_threads.get(zone)
        if thread is not None and thread.is_alive():
            return thread

        def refresh_loop():
            while True:
                try:
                    refresh_zone_graphs(zone)
                except Exception as error:
                    # Keep the background updater alive if one graph fails.
                    print(f"[ERROR] Graph refresh failed for {zone}: {error}")
                time.sleep(interval)

        thread = threading.Thread(
            target=refresh_loop,
            name=f"graph-refresh-{zone}",
            daemon=True,
        )
        _refresh_threads[zone] = thread
        thread.start()
        return thread
