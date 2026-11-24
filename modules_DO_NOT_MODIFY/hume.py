import random
import time
from pathlib import Path
import modules_DO_NOT_MODIFY.clock as clock

def _data_dir(zone):
    return Path(zone) / "data_DO_NOT_MODIFY"

def hum_adj(zone):
    hum_min = int(input("min: "))
    hum_max = int(input("max: "))
    if not 0 <= hum_min < hum_max <= 100:
        raise ValueError("Humidity values must satisfy 0 <= min < max <= 100.")
    (_data_dir(zone) / "presets" / "hum.txt").write_text(f"{hum_min}\n{hum_max}", encoding="utf-8")

def hum_monitor(zone):
    while True:
        (_data_dir(zone) / "hum_data.txt").write_text(str(random.randint(50, 100)), encoding="utf-8")
        time.sleep(300)

def hum_monitor_return(zone):
    return (_data_dir(zone) / "hum_data.txt").read_text(encoding="utf-8").strip()

def hum_act(zone):
    clock.iOrchid_clock(zone)
    clock.iOrchid_seasonal_clock(zone)
    data_dir = _data_dir(zone)
    season = (data_dir / "season(summer=1winter=2).txt").read_text(encoding="utf-8").strip()
    with (data_dir / "presets" / "hum.txt").open(encoding="utf-8") as settings:
        minimum = int(settings.readline().strip())
        maximum = int(settings.readline().strip())
    humidity = int((data_dir / "hum_data.txt").read_text(encoding="utf-8").strip())
    if season == "1":
        temperature = int((data_dir / "temp_data.txt").read_text(encoding="utf-8").strip())
        should_run = humidity <= minimum and temperature >= 30 and 9 <= int((data_dir / "time.txt").read_text()) <= 17
        print("[LOG] Humidifier turned on." if should_run else "[LOG] Humidifier turned off.")
    else:
        print("[LOG] Humidifier turned on (winter mode)." if humidity < minimum - 10 else "[LOG] Humidifier turned off (winter mode).")
