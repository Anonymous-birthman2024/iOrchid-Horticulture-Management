import random
import time

def temp_adj(zone):
    temp_min = int(input("min: "))
    temp_max = int(input("max: "))
    settingsFile = open(f"{zone}/data_DO_NOT_MODIFY/presets/temp.txt", "w")
    settingsFile.write(str(temp_min) + "\n" + str(temp_max))
    settingsFile.close()

def temp_monitor(zone):
    while True:
        dataFile = open(f"{zone}/data_DO_NOT_MODIFY/temp_data.txt", "w")
        tempData = random.randint(0, 40)
        dataFile.write(str(tempData))
        dataFile.close()
        time.sleep(300)
        
        
        
def temp_act(zone):
    presetsFile = open(f"{zone}/data_DO_NOT_MODIFY/presets/temp.txt", "r")
    dataFile = open(f"{zone}/data_DO_NOT_MODIFY/temp_data.txt", "r")
    minTempPreset = int(presetsFile.readline().strip())
    maxTempPreset = int(presetsFile.readline().strip())
    tempData = int(dataFile.readline().strip())
    if tempData < minTempPreset:
        if tempData < 11:
            print("[FATAL] YOUR PLANT(S) IS FREEZING! TEND TO IT IMMEDIATELY!")
        print("[LOG] Heater is on.")
    elif tempData > maxTempPreset:
        print("[LOG] Heater is off.")
    else:
        print("[LOG] Temperature is within acceptable range. Heater is off.")
        
        
# temp_monitor("Zone1")
# temp_monitor("Zone2")
# temp_monitor("Zone3")
# temp_monitor("Zone4")
# temp_monitor("Zone5")
# temp_monitor("Zone6")
