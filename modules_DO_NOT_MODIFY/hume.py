import random
import time

from modules_DO_NOT_MODIFY.sensor_storage import append_history, write_current_reading
import modules_DO_NOT_MODIFY.clock as clock


def hum_adj(zone):
    hum_min = int(input("min: "))
    hum_max = int(input("max: "))
    if not 0 <= hum_min < hum_max <= 100:
        raise ValueError("Humidity limits must satisfy 0 <= min < max <= 100.")
    with open(f"{zone}/data_DO_NOT_MODIFY/presets/hum.txt", "w", encoding="utf-8") as f:
        f.write(f"{hum_min}\n{hum_max}\n")


def hum_monitor(zone):
    """Generate simulated humidity readings (replace with hardware input when available)."""
    while True:
        humidity = random.randint(50, 100)
        try:
            write_current_reading(zone, "hum_data.txt", humidity)
            append_history(zone, "hume", humidity)
        except OSError as exc:
            print(f"[WARN] {zone}: could not save humidity reading: {exc}")
        time.sleep(300)


def hum_monitor_return(zone):
    with open(f"{zone}/data_DO_NOT_MODIFY/hum_data.txt", "r", encoding="utf-8") as data_file:
        return data_file.readline().strip()


def hum_act(zone):
    clock.iOrchid_clock(zone)
    clock.iOrchid_seasonal_clock(zone)

    base = f"{zone}/data_DO_NOT_MODIFY"
    with open(f"{base}/season(summer=1winter=2).txt", "r", encoding="utf-8") as f:
        season = f.read().strip()
    with open(f"{base}/presets/hum.txt", "r", encoding="utf-8") as f:
        limits = [int(line.strip()) for line in f if line.strip()]
    if len(limits) != 2:
        print(f"[WARN] {zone}: humidity preset must contain minimum and maximum values.")
        return
    hum_min, hum_max = limits

    with open(f"{base}/hum_data.txt", "r", encoding="utf-8") as f:
        humidity = int(f.read().strip())

    if not 0 <= humidity <= 100:
        print(f"[WARN] {zone}: invalid humidity reading {humidity}%.")
        return

    if humidity > hum_max:
        print(f"[WARN] Humidity too high ({humidity}%). Humidifier off; increase ventilation.")
    elif humidity < hum_min:
        # Winter mode permits a lower humidity before requesting humidification.
        threshold = max(0, hum_min - 10) if season == "2" else hum_min
        if humidity < threshold:
            print("[LOG] Humidifier turned on (winter mode)." if season == "2"
                  else "[LOG] Humidifier turned on.")
        else:
            print("[LOG] Humidity acceptable for winter mode; humidifier off.")
    else:
        print("[LOG] Humidity is within acceptable range. Humidifier off.")
