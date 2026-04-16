import random
import time
import modules_DO_NOT_MODIFY.clock as clock
import threading
# import clock

def hum_adj(zone):
    hum_min = int(input("min: "))
    hum_max = int(input("max: "))
    with open(f"{zone}/data_DO_NOT_MODIFY/presets/hum.txt", "w") as f:
        f.write(str(hum_min) + "\n" + str(hum_max))

def hum_monitor(zone):
    while True:
        dataFile = open(f"{zone}/data_DO_NOT_MODIFY/hum_data.txt", "w")
        dataFile.write(str(random.randint(50, 100)))
        dataFile.close()
        time.sleep(300)

# def start_hum_monitor(zone):
#     thread = threading.Thread(target=hum_monitor, args=(zone,), daemon=True)
#     thread.start()

def hum_act(zone):
    clock.iOrchid_clock(zone)
    clock.iOrchid_seasonal_clock(zone)
    season = open(f"{zone}/data_DO_NOT_MODIFY/season(summer=1winter=2).txt", "r").read().strip()
    if season == "1":  # If it's summer
        with open(f"{zone}/data_DO_NOT_MODIFY/time.txt", "r") as timeFile, \
            open(f"{zone}/data_DO_NOT_MODIFY/presets/hum.txt", "r") as preferenceFile, \
            open(f"{zone}/data_DO_NOT_MODIFY/hum_data.txt", "r") as dataFile, \
            open(f"{zone}/data_DO_NOT_MODIFY/temp_data.txt", "r") as tempdataFile:

            current_hour = int(timeFile.read())
            preference = int(preferenceFile.readline())
            humidity = int(dataFile.read())
            temperature = int(tempdataFile.read())

            if humidity <= preference and temperature >= 30 and 9 <= current_hour <= 17:
                print("[LOG] Humidifier turned on.")
            else:
                print("[LOG] Humidifier turned off.")
    else:
        print("[LOG] It's winter, no need to adjust humidity.")
        
# start_hum_monitor("Zone1")
# start_hum_monitor("Zone2")
# start_hum_monitor("Zone3")
# start_hum_monitor("Zone4")
# start_hum_monitor("Zone5")
# start_hum_monitor("Zone6")