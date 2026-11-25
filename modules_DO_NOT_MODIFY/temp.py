import random
import threading
import time

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


def temp_adj(zone):
    try:
        temp_min = int(input("Minimum temperature (°C): "))
        temp_max = int(input("Maximum temperature (°C): "))
        save_preset(zone, "temp", temp_min, temp_max)
    except ValueError as error:
        print(f"[ERROR] Invalid temperature preset: {error}")


def temp_monitor(zone):
    while True:
        temperature = random.randint(0, 40)
        write_current_reading(zone, "temp_data.txt", temperature)
        append_history(zone, "temp", temperature)
        time.sleep(MONITOR_INTERVAL)


def temp_monitor_return(zone):
    return read_integer(zone_data_dir(zone) / "temp_data.txt")


def start_temp_monitor(zone):
    """Start at most one temperature-monitor thread per zone in this process."""
    with _monitor_lock:
        thread = _monitor_threads.get(zone)
        if thread is not None and thread.is_alive():
            return thread

        thread = threading.Thread(
            target=temp_monitor,
            args=(zone,),
            name=f"temperature-monitor-{zone}",
            daemon=True,
        )
        _monitor_threads[zone] = thread
        thread.start()
        return thread


def temp_act(zone):
    preset = read_preset(zone, "temp")
    temperature = temp_monitor_return(zone)

    if preset is None or temperature is None:
        print("[ERROR] Temperature reading or temperature presets are missing/invalid.")
        return

    min_temp, max_temp = preset

    if temperature < min_temp:
        if temperature < 11:
            print("[FATAL] YOUR PLANT(S) IS FREEZING! TEND TO IT IMMEDIATELY!")
        print("[LOG] Heater is on.")
    elif temperature > max_temp:
        print("[LOG] Cooling system activated.")
    else:
        print("[LOG] Temperature is within acceptable range. Climate control is off.")
