import random
import time
from pathlib import Path

def _data_path(zone):
    return Path(zone) / "data_DO_NOT_MODIFY"

def temp_adj(zone):
    temp_min = int(input("min: "))
    temp_max = int(input("max: "))
    if temp_min >= temp_max:
        raise ValueError("Minimum temperature must be lower than maximum temperature.")
    (_data_path(zone) / "presets" / "temp.txt").write_text(f"{temp_min}\n{temp_max}", encoding="utf-8")

def temp_monitor(zone):
    while True:
        (_data_path(zone) / "temp_data.txt").write_text(str(random.randint(0, 40)), encoding="utf-8")
        time.sleep(300)

def temp_monitor_return(zone):
    return (_data_path(zone) / "temp_data.txt").read_text(encoding="utf-8").strip()

def temp_act(zone):
    data_dir = _data_path(zone)
    with (data_dir / "presets" / "temp.txt").open(encoding="utf-8") as presets_file:
        min_temp = int(presets_file.readline().strip())
        max_temp = int(presets_file.readline().strip())
    temp_data = int((data_dir / "temp_data.txt").read_text(encoding="utf-8").strip())
    if temp_data < min_temp:
        if temp_data < 11:
            print("[FATAL] YOUR PLANT(S) IS FREEZING! TEND TO IT IMMEDIATELY!")
        print("[LOG] Heater is on.")
    elif temp_data > max_temp:
        print("[LOG] Cooling system activated.")
    else:
        print("[LOG] Temperature is within acceptable range. Climate control is off.")
