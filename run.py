'''
RUN THIS FILE ONCE ON THE SERVER ONLY!!!
To quit, connect to the server via SSH and press 'q' to quit the program. This will also stop the web server.
'''

from pathlib import Path
import time
from datetime import datetime
import subprocess

import modules_DO_NOT_MODIFY.temp as temp
import modules_DO_NOT_MODIFY.hume as hume
import modules_DO_NOT_MODIFY.light as light
import modules_DO_NOT_MODIFY.clock as clock
import pynput.keyboard as keyboard


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "setupTimer.iOrchidConfig"


with CONFIG_PATH.open("r", encoding="utf-8") as f:
    setuped = int(f.read().strip())
print(setuped)


def setup():
    global setuped
    invite_message = '''
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
        CONFIG_PATH.write_text("1", encoding="utf-8")

    else:
        pass


def data_logging(dataType, zone):
    now = datetime.now()
    time_stamp = now.strftime("%Y%m%d-%H%M")
    data_path = BASE_DIR / zone / "data_DO_NOT_MODIFY" / f"{dataType}_data.txt"
    with data_path.open("r", encoding="utf-8") as src:
        print(f"[INFO {time_stamp}] {dataType}:{src.read()}")


running = True


def on_press(key):
    global running
    if key == keyboard.KeyCode.from_char('q'):
        print("[INFO] Q pressed, shutting down loop...")
        running = False
        return False


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
    server_proc = subprocess.Popen(
        ["/bin/bash", str(BASE_DIR / "activateServer.sh")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )

    print("[LOG] iOrchid server started at port localhost:5002.")

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
        time.sleep(1)

    try:
        listener.stop()
    except Exception:
        pass

    try:
        if 'server_proc' in locals() and server_proc.poll() is None:
            print("[INFO] Stopping iOrchid server...")
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()
    except Exception as e:
        print(f"[WARN] Error shutting down server process: {e}")


main()