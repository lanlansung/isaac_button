print "Hello, isaac!"

import os
import time
import threading
import mraa
from datetime import datetime, timedelta, tzinfo
from twitter import *
from mqtt_client import MqttClient

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# Twitter
auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=auth)

class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'JST'

class ButtonState:
    pressing = False
    tweeting = False

b_state = ButtonState()

def reset_b_pressing():
    b_state.pressing = False

def reset_b_tweeting():
    b_state.tweeting = False

def tweet(time, button_size):
    print time
    print button_size
    message = button_size + " button pressed at " + time.strftime("%H:%M:%S.%f") + ". Reply me to ring the buzzer in the show space of PioneersAsia."
    print "message: " + message
    filename = button_size + "_button.jpg"
    media_id = upload_image(filename)
    twitter.statuses.update(status=message, media_ids=media_id)
    print 'tweeted'
    b_state.tweeting = False

def on_click(args):
    print(b_state.pressing)
    if not b_state.pressing:
        b_state.pressing = True
        t = threading.Timer(0.2, reset_b_pressing)
        t.start()
        print("clicked!")
        time = datetime.now(tz=JST())
        button_size = os.environ['SIZE']
        try:
            client.publish('/button/' + button_size, "Hello, now: " + str(time))
        except Exception as e:
            print traceback.format_exc()
        if not b_state.tweeting:
            b_state.tweeting = True
            tt = threading.Thread(target=tweet, args=(time, button_size,))
            tt.start()
    else:
        print("chatter!")

def on_connect(client, userdata, rc):
    print("Connected MQTT with result code "+str(rc))
    b.isr(mraa.EDGE_FALLING, on_click, on_click)

def upload_image(filename):
    t_up = Twitter(domain='upload.twitter.com', auth=auth)
    with open(filename, "rb") as imagefile:
        imagedata = imagefile.read()
    m_id = t_up.media.upload(media=imagedata)["media_id_string"]
    print m_id
    return m_id

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

