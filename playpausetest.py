import RPi.GPIO as GPIO
import time

import signal
import sys
from os import system, path

from mpd import MPDClient

class Button(object):
    '''
       Buttons class. Includes associated pin, sound playback and associated button color.
    '''
    def __init__(self, pin, color, playlist):
        self.pin = pin
        self.color = color
        self.playlist = playlist
        self.uri = None
        self.status = True #True means unpressed, False means pressed

    def playsound(self, channel):
        client.clear()
        client.add(self.uri)
        client.play()
        pass

    def seturi(self, uri):
        self.uri = uri

    def updateStatus(self):
        self.status = GPIO.input(self.pin)
        pass

    def reportStatus(self):
        return self.status

    def reportColor(self):
        return self.color

#Declare all buttons
BUTTON_PINS = [
                Button(6, 'Blue', 'Both Frozens'),
                Button(12, 'Green', 'None'),
                Button(13, 'Yellow', 'None'),
                Button(16, 'White', 'None')
                ]
STOP_BUTTON = 5
def stopcallback(channel):
    client.pause()
    client.close()
    client.disconnect()

BUTTON_PINS[0].seturi('spotify:playlist:6gBXZmySP7a6n4PZJhaqYO') #Both Frozens Playlist

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    client = MPDClient()
    client.connect("localhost", 6600)
    GPIO.setmode(GPIO.BCM)

    #setup playback buttons
    for btn in BUTTON_PINS:
        GPIO.setup(btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn.pin, GPIO.FALLING, btn.playsound, bouncetime=100)

    #setup stop button
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(STOP_BUTTON, GPIO.FALLING, stopcallback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
