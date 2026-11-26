"""iOrchid controller entry point. Run this file once on the server. Stop with Ctrl+C."""
from pathlib import Path
from datetime import datetime
import subprocess
import threading
import time

import modules_DO_NOT_MODIFY.temp as temp
import modules_DO_NOT_MODIFY.hume as hume
import modules_DO_NOT_MODIFY.light as light
import modules_DO_NOT_MODIFY.grapher as grapher

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "setupTimer.iOrchidConfig"
ZONES = [f"Zone{i}" for i in range(1, 7)]
running = True

def graphInit():
    """Create initial graph snapshots without blocking for historical samples."""
    for zone in ZONES:
        for graph in (grapher.humeGrapherWeek, grapher.humeGrapherMonth,
                      grapher.lightGrapherWeek, grapher.lightGrapherMonth,
                      grapher.tempGrapherWeek, grapher.tempGrapherMonth):
            try:
                graph(zone)
            except (OSError, ValueError):
                # A zone may not have a valid reading until its monitor starts.
                print(f"[WARN] Skipping initial graph for {zone}; sensor data unavailable.")

def setup():
    try:
        setuped = int(CONFIG_PATH.read_text(encoding="utf-8").strip() or "0")
    except (FileNotFoundError, ValueError):
        setuped = 0
    if setuped:
        return
    print("Welcome to iOrchid Horticulture Management setup.")
    for zone in ZONES:
        print(f"Humidity settings for {zone}")
        hume.hum_adj(zone)
    for zone in ZONES:
        print(f"Temperature settings for {zone}")
        temp.temp_adj(zone)
    CONFIG_PATH.write_text("1", encoding="utf-8")

def data_logging(data_type, zone):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    path = BASE_DIR / zone / "data_DO_NOT_MODIFY" / f"{data_type}_data.txt"
    try:
        value = path.read_text(encoding="utf-8").strip()
        print(f"[INFO {timestamp}] {zone} {data_type}: {value}")
    except OSError as exc:
        print(f"[WARN] Cannot read {path}: {exc}")

def main():
    global running
    import os
    os.chdir(BASE_DIR)
    setup()

    # Start sensor simulators once per zone. Threads exit with the process.
    monitor_threads = []
    for zone in ZONES:
        for monitor in (hume.hum_monitor, temp.temp_monitor, light.light_monitor):
            thread = threading.Thread(target=monitor, args=(zone,), daemon=True)
            thread.start()
            monitor_threads.append(thread)
    time.sleep(0.2)

    server_proc = subprocess.Popen(
        ["/bin/bash", str(BASE_DIR / "activateServer.sh")],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    print("[LOG] iOrchid server started on port 5002.")
    graphInit()

    try:
        while running:
            for zone in ZONES:
                for data_type, action in (
                    ("hum", hume.hum_act),
                    ("temp", temp.temp_act),
                    ("light", light.light_act),
                ):
                    data_logging(data_type, zone)
                    action(zone)
            time.sleep(1)
    except KeyboardInterrupt:
        print("[INFO] Shutdown requested.")
    finally:
        running = False
        if server_proc.poll() is None:
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()

if __name__ == "__main__":
    main()
