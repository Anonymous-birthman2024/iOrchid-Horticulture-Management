import random
import threading
import time

import modules_DO_NOT_MODIFY.clock as clock
from modules_DO_NOT_MODIFY.sensor_storage import (
    append_history,
    read_integer,
    read_preset,
    save_preset,
    write_current_reading,
    zone_data_dir,
)

MONITOR_INTERVAL = 300
_monitor_threads = {}
_monitor_lock = threading.Lock()


def hum_adj(zone):
    try:
        hum_min = int(input("Minimum humidity (%): "))
        hum_max = int(input("Maximum humidity (%): "))
        save_preset(zone, "hum", hum_min, hum_max)
    except ValueError as error:
        print(f"[ERROR] Invalid humidity preset: {error}")


def hum_monitor(zone):
    while True:
        humidity = random.randint(50, 100)
        write_current_reading(zone, "hum_data.txt", humidity)
        append_history(zone, "hum", humidity)
        time.sleep(MONITOR_INTERVAL)


def hum_monitor_return(zone):
    return read_integer(zone_data_dir(zone) / "hum_data.txt")


def start_hum_monitor(zone):
    """Start at most one humidity-monitor thread per zone in this process."""
    with _monitor_lock:
        thread = _monitor_threads.get(zone)
        if thread is not None and thread.is_alive():
            return thread

        thread = threading.Thread(
            target=hum_monitor,
            args=(zone,),
            name=f"humidity-monitor-{zone}",
            daemon=True,
        )
        _monitor_threads[zone] = thread
        thread.start()
        return thread


def hum_act(zone):
    try:
        clock.iOrchid_clock(zone)
        clock.iOrchid_seasonal_clock(zone)

        season_path = zone_data_dir(zone) / "season(summer=1winter=2).txt"
        season = season_path.read_text(encoding="utf-8").strip()

        preset = read_preset(zone, "hum")
        humidity = hum_monitor_return(zone)

        if preset is None or humidity is None:
            print("[ERROR] Humidity reading or humidity presets are missing/invalid.")
            return

        hum_min, _hum_max = preset

        if season == "1":
            time_value = read_integer(zone_data_dir(zone) / "time.txt")
            temperature = read_integer(zone_data_dir(zone) / "temp_data.txt")

            if time_value is None or temperature is None:
                print("[ERROR] Time or temperature data is missing/invalid.")
                return

            if humidity <= hum_min and temperature >= 30 and 9 <= time_value <= 17:
                print("[LOG] Humidifier turned on.")
            else:
                print("[LOG] Humidifier turned off.")

        elif season == "2":
            if humidity < hum_min - 10:
                print("[LOG] Humidifier turned on (winter mode).")
            else:
                print("[LOG] Humidifier turned off (winter mode).")
        else:
            print(f"[ERROR] Unknown season value: {season!r}")

    except OSError as error:
        print(f"[ERROR] Unable to access humidity control files: {error}")
