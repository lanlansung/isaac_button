print "Hello, isaac!"

import os
import time
import datetime
import threading
import mraa
from mqtt_client import MqttClient

class ButtonState:
    pressing = False

b_state = ButtonState()

def reset_b_pressing():
   b_state.pressing = False 

def on_click(args):
    print(b_state.pressing)
    if not b_state.pressing:
        b_state.pressing = True
        print("clicked!")
        client.publish('/button', "Hello, now: " + str(datetime.datetime.now()))
        t = threading.Timer(0.2, reset_b_pressing)
        t.start()
    else:
        print("chatter!")

def on_connect(client, userdata, rc):
    print("Connected MQTT with result code "+str(rc))
    b.isr(mraa.EDGE_FALLING, on_click, on_click)

if __name__ == '__main__':
    # Button
    b = mraa.Gpio(14)
    b.dir(mraa.DIR_IN)
    b.mode(mraa.MODE_PULLUP)

    # MQTT
    client = MqttClient(os.environ['MQTT_URL'])
    client.on_connect = on_connect
    client.connect()
    client.loop_forever()
