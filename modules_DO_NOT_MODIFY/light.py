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


def light_adj(zone):
    try:
        light_min = int(input("Minimum light intensity (lux): "))
        light_max = int(input("Maximum light intensity (lux): "))
        save_preset(zone, "light", light_min, light_max)
    except ValueError as error:
        print(f"[ERROR] Invalid light preset: {error}")


def light_monitor(zone):
    while True:
        light_intensity = random.randint(5000, 40000)
        write_current_reading(zone, "light_data.txt", light_intensity)
        append_history(zone, "light", light_intensity)
        time.sleep(MONITOR_INTERVAL)


def light_monitor_return(zone):
    return read_integer(zone_data_dir(zone) / "light_data.txt")


def start_light_monitor(zone):
    """Start at most one light-monitor thread per zone in this process."""
    with _monitor_lock:
        thread = _monitor_threads.get(zone)
        if thread is not None and thread.is_alive():
            return thread

        thread = threading.Thread(
            target=light_monitor,
            args=(zone,),
            name=f"light-monitor-{zone}",
            daemon=True,
        )
        _monitor_threads[zone] = thread
        thread.start()
        return thread


def light_act(zone):
    preset = read_preset(zone, "light")
    light_intensity = light_monitor_return(zone)

    if preset is None or light_intensity is None:
        print("[ERROR] Light reading or light presets are missing/invalid.")
        return

    light_min, light_max = preset
    print(zone)

    if light_intensity < light_min:
        print("[LOG] Light intensity too low. Lamp on to increase light intensity.")
    elif light_intensity > light_max:
        print("[LOG] Light intensity too high. Lamp off. Please check surroundings.")
    else:
        print("[LOG] Light intensity OK.")
