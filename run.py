import modules_DO_NOT_MODIFY.temp as temp
import modules_DO_NOT_MODIFY.hume as hume
import modules_DO_NOT_MODIFY.light as light
import modules_DO_NOT_MODIFY.clock as clock
import time
from datetime import datetime
from pynput import keyboard


f = open("setupTimer.iOrchidConfig", "r")
setuped = int(f.read())
print(setuped)
f.close()

def setup():
    global setuped
    invite_message='''
Welcome to iOrchid Horticulture Management. This wizard will walk you through the steps needed
to set up this software.
'''
    if setuped == 0:
        print(invite_message)
        time.sleep(1)
        print("Step 1. Establish your values")
        time.sleep(1)
        print("The wizard will now ask you a few questions about your orchid's environment requirements.")
        time.sleep(1)
        print("Humidity Values. Fill out for 6 different zones")
        time.sleep(1)
        hume.hum_adj("Zone1")
        print("Saving Values...")
        time.sleep(2)
        hume.hum_adj("Zone2")
        print("Saving Values...")
        time.sleep(2)
        hume.hum_adj("Zone3")
        print("Saving Values...")
        time.sleep(2)
        hume.hum_adj("Zone4")
        print("Saving Values...")
        time.sleep(2)
        hume.hum_adj("Zone5")
        print("Saving Values...")
        time.sleep(2)
        hume.hum_adj("Zone6")
        print("Saving Values...")
        time.sleep(2)
        print("Temperature Values. Fill out for 6 different zones")
        time.sleep(1)
        temp.temp_adj("Zone1")
        print("Saving Values...")
        time.sleep(2)
        temp.temp_adj("Zone2")
        print("Saving Values...")
        time.sleep(2)
        temp.temp_adj("Zone3")
        print("Saving Values...")
        time.sleep(2)
        temp.temp_adj("Zone4")
        print("Saving Values...")
        time.sleep(2)
        temp.temp_adj("Zone5")
        print("Saving Values...")
        time.sleep(2)
        temp.temp_adj("Zone6")
        print("Saving Values...")
        time.sleep(2)
        save = open("setupTimer.iOrchidConfig", "w")
        save.write("1")
        save.close()

    else:
        pass

def data_logging(dataType, zone):
    now = datetime.now()
    time = now.strftime("%Y%m%d-%H%M")
    src = open(f"{zone}/data_DO_NOT_MODIFY/{dataType}_data.txt")
    print(f"[INFO {time}] {dataType}:{src.read()}")

running = True

def on_press(key):
    global running
    if key == keyboard.KeyCode.from_char('q'):
        print("[INFO] Q pressed, shutting down loop...")
        running = False
        return False  # Stop the listener

def stop_loop(e):
    global running
    print("[INFO] Q pressed, shutting down loop...")
    running = False



def main():
    setup()
    print("Welcome! The software will now test it's logging capabilities.")
    time.sleep(1)
    print("[INFO YYYYMMDD-HHMM] This is a data message.")
    print("[LOG] This is a message that indicates a status of something")
    print("[WARN] This is a message that warns you of a hazard.")
    print("[FATAL] This message warns about hazards that will hurt your crop.")

    # Start keyboard listener for 'q' to quit
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while running:
        data_logging("hum", "Zone1")
        hume.hum_act("Zone1")
        data_logging("temp", "Zone1")
        temp.temp_act("Zone1")
        data_logging("light", "Zone1")
        light.light_act("Zone1")
        time.sleep(1)
        data_logging("hum", "Zone2")
        hume.hum_act("Zone2")
        data_logging("temp", "Zone2")
        temp.temp_act("Zone2")
        data_logging("light", "Zone2")
        light.light_act("Zone2")
        time.sleep(1)
        data_logging("hum", "Zone3")
        hume.hum_act("Zone3")
        data_logging("temp", "Zone3")
        temp.temp_act("Zone3")
        data_logging("light", "Zone3")
        light.light_act("Zone3")
        time.sleep(1)
        data_logging("hum", "Zone4")
        hume.hum_act("Zone4")
        data_logging("temp", "Zone4")
        temp.temp_act("Zone4")
        data_logging("light", "Zone4")
        light.light_act("Zone4")
        time.sleep(1)
        data_logging("hum", "Zone5")
        hume.hum_act("Zone5")
        data_logging("temp", "Zone5")
        temp.temp_act("Zone5")
        data_logging("light", "Zone5")
        light.light_act("Zone5")
        time.sleep(1)
        data_logging("hum", "Zone6")
        hume.hum_act("Zone6")
        data_logging("temp", "Zone6")
        temp.temp_act("Zone6")
        data_logging("light", "Zone6")
        light.light_act("Zone6")




    


        
        
main()