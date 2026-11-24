import random
import time
from pathlib import Path

def _data_dir(zone):
    return Path(zone) / "data_DO_NOT_MODIFY"

def light_adj(zone):
    light_min = int(input("min: "))
    light_max = int(input("max: "))
    if light_min >= light_max:
        raise ValueError("Minimum light level must be lower than maximum light level.")
    (_data_dir(zone) / "presets" / "light.txt").write_text(f"{light_min}\n{light_max}", encoding="utf-8")

def light_monitor(zone):
    while True:
        (_data_dir(zone) / "light_data.txt").write_text(str(random.randint(5000, 40000)), encoding="utf-8")
        time.sleep(300)

def light_monitor_return(zone):
    return (_data_dir(zone) / "light_data.txt").read_text(encoding="utf-8").strip()

def light_act(zone):
    data_dir = _data_dir(zone)
    intensity = int((data_dir / "light_data.txt").read_text(encoding="utf-8").strip())
    with (data_dir / "presets" / "light.txt").open(encoding="utf-8") as settings:
        minimum = int(settings.readline().strip())
        maximum = int(settings.readline().strip())
    if intensity < minimum:
        print("[LOG] Light intensity too low. Lamp on to increase light intensity.")
    elif intensity > maximum:
        print("[LOG] Light intensity too high. Lamp off. Please check surroundings.")
    else:
        print("[LOG] Light intensity OK.")
