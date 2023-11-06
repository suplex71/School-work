from Occupancy_Aggregate.API.app import ReceiverListener
from Lights_Aggregate.API.app import LightListener
from Cleaning_Aggregate.API.app import CleaningListener
from BMS.app import BMSListener
from Gateway.app import GatewayListener
import threading
import requests
from Credentials import storecreds as cfg
import time

def start_apis():
    # Occupancy Aggregate
    rl = ReceiverListener()
    thread_receiver = threading.Thread(target=rl.start_listening)
    thread_receiver.start()
    # Lights Aggregate
    ll = LightListener()
    thread_light = threading.Thread(target=ll.start_listening)
    thread_light.start()
    # Cleaning Aggregate
    cl = CleaningListener()
    thread_cleaning = threading.Thread(target=cl.start_listening)
    thread_cleaning.start()

    # Gateway
    gw = GatewayListener()
    thread_gw = threading.Thread(target=gw.start_listening)
    thread_gw.start()

    # BMS
    bms = BMSListener()
    thread_bms = threading.Thread(target=bms.start_listening)
    thread_bms.start()

def start_receiver():
    requests.post(f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/start")

def start_light():
    requests.post(f"http://{cfg.httprequests['light_ms']}:{cfg.httprequests['light_port']}/start")

def start_cleaning():
    requests.post(f"http://{cfg.httprequests['cleaning_ms']}:{cfg.httprequests['cleaning_port']}/start")

thread_apis = threading.Thread(target=start_apis)
thread_apis.start()

time.sleep(5)

thread_receiver = threading.Thread(target=start_receiver)
thread_receiver.start()

# thread_light = threading.Thread(target=start_light)
# thread_light.start()

# thread_cleaning = threading.Thread(target=start_cleaning)
# thread_cleaning.start()

