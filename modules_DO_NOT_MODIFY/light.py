import random
import time


def light_adj(zone):
    light_min = int(input("min: "))
    light_max = int(input("max: "))
    with open(f"{zone}/data_DO_NOT_MODIFY/presets/light.txt", "w") as f:
        f.write(str(light_min) + "\n" + str(light_max))

def light_monitor(zone):
    while True:
        dataFile = open(f"{zone}/data_DO_NOT_MODIFY/light_data.txt", "w")
        dataFile.write(str(random.randint(5000, 40000)))
        dataFile.close()
        time.sleep(300)

def light_act(zone):
    print(zone)
    f = open(f"{zone}/data_DO_NOT_MODIFY/light_data.txt", "r")
    lightIntensity = f.readlines()[0]
    lightRange = open(f"{zone}/data_DO_NOT_MODIFY/presets/light.txt", "r")
    lightMin = lightRange.readline()
    lightMax = lightRange.readline()


    if int(lightIntensity) < int(lightMax) and int(lightIntensity) > int(lightMin):
        print("[LOG] Light Intensity OK")
    if int(lightIntensity) < int(lightMin):
        print("[LOG] Light Intensity too low. Lamp on to increase light intensity")
    if int(lightMax) < int(lightIntensity):
        print("[LOG] Light Intensity too high. Lamp off. Please check surroundings.")

# light_monitor("Zone1")
# light_monitor("Zone2")
# light_monitor("Zone3")
# light_monitor("Zone4")
# light_monitor("Zone5")
# light_monitor("Zone6")
