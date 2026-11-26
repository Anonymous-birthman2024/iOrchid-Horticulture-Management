import random
import time


def temp_adj(zone):
    temp_min = int(input("min: "))
    temp_max = int(input("max: "))
    if temp_min >= temp_max:
        raise ValueError("Minimum temperature must be lower than maximum temperature.")
    with open(f"{zone}/data_DO_NOT_MODIFY/presets/temp.txt", "w", encoding="utf-8") as settings_file:
        settings_file.write(f"{temp_min}\n{temp_max}\n")


def temp_monitor(zone):
    """
    Simulate a temperature sensor using that zone's configured limits.

    This is deliberately a simulator, not a physical sensor interface. It
    avoids generating arbitrary 0-40 C values that trigger misleading
    freezing/overheating alarms in normal test runs.
    """
    preset_path = f"{zone}/data_DO_NOT_MODIFY/presets/temp.txt"
    data_path = f"{zone}/data_DO_NOT_MODIFY/temp_data.txt"
    while True:
        try:
            with open(preset_path, "r", encoding="utf-8") as preset_file:
                limits = [int(line.strip()) for line in preset_file if line.strip()]
            if len(limits) != 2 or limits[0] >= limits[1]:
                raise ValueError("invalid temperature preset")
            temp_data = random.randint(limits[0], limits[1])
            with open(data_path, "w", encoding="utf-8") as data_file:
                data_file.write(str(temp_data))
        except (OSError, ValueError) as exc:
            print(f"[WARN] {zone}: temperature simulator could not read presets: {exc}")
        time.sleep(300)


def temp_monitor_return(zone):
    with open(f"{zone}/data_DO_NOT_MODIFY/temp_data.txt", "r", encoding="utf-8") as data_file:
        return data_file.readline().strip()


def temp_act(zone):
    base = f"{zone}/data_DO_NOT_MODIFY"
    try:
        with open(f"{base}/presets/temp.txt", "r", encoding="utf-8") as presets_file:
            limits = [int(line.strip()) for line in presets_file if line.strip()]
        with open(f"{base}/temp_data.txt", "r", encoding="utf-8") as data_file:
            temp_data = float(data_file.read().strip())
        if len(limits) != 2 or limits[0] >= limits[1]:
            raise ValueError("temperature preset must contain valid minimum and maximum values")
    except (OSError, ValueError) as exc:
        print(f"[WARN] {zone}: cannot evaluate temperature: {exc}")
        return

    min_temp, max_temp = limits
    if temp_data < min_temp:
        if temp_data < 11:
            print("[FATAL] YOUR PLANT(S) IS FREEZING! TEND TO IT IMMEDIATELY!")
        print("[LOG] Heater is on.")
    elif temp_data > max_temp:
        print("[LOG] Cooling system activated.")
    else:
        print("[LOG] Temperature is within acceptable range. Climate control is off.")
