import RPi.GPIO as GPIO
import time

import signal
import sys
from os import system, path

class Button(object):
    '''
       Buttons class. Includes associated pin, sound playback and associated button color.
    '''
    def __init__(self, pin, color, sound):
        self.pin = pin
        self.color = color
        self.sound = sound
        self.base_path = '~/projects/PiMusicBoxTest/'
        self.status = True #True means unpressed, False means pressed

    def playsound(self, channel):
        system('aplay -q {}'.format(self.base_path + self.sound + '.wav'))
        pass

    def updateStatus(self):
        self.status = GPIO.input(self.pin)
        pass

    def reportStatus(self):
        return self.status

    def reportColor(self):
        return self.color

#Declare all buttons
BUTTON_PINS = [
                Button(5, 'Red', 'moo'),
                Button(6, 'Blue', 'tada'),
                Button(12, 'Green', 'tada'),
                Button(13, 'Yellow', 'rooster'),
                Button(16, 'White', 'tada')
                ]

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    for btn in BUTTON_PINS:
        GPIO.setup(btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn.pin, GPIO.FALLING, btn.playsound, bouncetime=75)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
