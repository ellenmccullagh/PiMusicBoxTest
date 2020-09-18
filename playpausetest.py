import RPi.GPIO as GPIO
import time

import signal
import sys
from os import system, path

from mpd import MPDClient


class Button(object):
    '''
       Buttons that correspond to playlists
    '''
    def __init__(self, pin, color, playlist, uri = None):
        self.pin = pin
        self.color = color
        self.playlist = playlist
        self.uri = uri
        self.status = True #True means unpressed, False means pressed

    def playsound(self, channel): #if the current playlist corresponds to this button, skip to the next track. Otherwise change the playlist and begin playback
        global currentplaylist

        client = MPDClient()
        client.connect("localhost", 6600)

        if currentplaylist == self.playlist:
            client.next()
            print('{} next track'.format(self.playlist))
        else:
            client.clear()
            client.add(self.uri)
            client.play()
            print('{} playing'.format(self.playlist))
            currentplaylist = self.playlist

        client.close()
        client.disconnect()

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
                Button(6, 'Blue', 'Both Frozens', 'spotify:playlist:6gBXZmySP7a6n4PZJhaqYO'),
                Button(12, 'Green', 'Miles favorites', 'spotify:playlist:1eKf1Q2I7GKi3BfHTNL4Dt'),
                Button(13, 'Yellow', 'Lullabies for Miles', 'spotify:playlist:22xETQTI3B6RzEdgBqPqXS'),
                Button(16, 'White', 'This Is Raffi', 'spotify:playlist:37i9dQZF1DX4dWEvmDfGoP')
                ]

'''
Declare pause/resume toggle button pin and callback function
'''
STOP_BUTTON = 5
def stopcallback(channel):
    client = MPDClient()
    client.connect("localhost", 6600)

    if client.status()['state'] == 'play': #playlist is already playing
        client.pause()
        print('Paused')
    elif client.status()['state'] == 'pause': #playlist is paused
        client.play()
        print('Resumed')
    else: #playlist is stopped
        pass
    client.close()
    client.disconnect()


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    currentplaylist = 'None'

    #setup playback buttons
    for btn in BUTTON_PINS:
        GPIO.setup(btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn.pin, GPIO.FALLING, btn.playsound, bouncetime=150)

    #setup stop button
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(STOP_BUTTON, GPIO.FALLING, stopcallback, bouncetime=150)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
