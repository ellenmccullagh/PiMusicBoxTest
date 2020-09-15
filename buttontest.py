import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
from os import path, system

BUTTON_PINS = {
                5: 'Red',
                6: 'Blue',
                12: 'Green',
                13: 'Yellow',
                16: 'White'
                }

file_path = '~/projects/PiMusicBoxTest/tada.wav'


for pin in BUTTON_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        input_states = [(BUTTON_PINS[pin], GPIO.input(pin)) for pin in BUTTON_PINS]
        for state in input_states:
                if state[1] == False:
                        print('Button {} Pressed'.format(state[0]))
                        system('aplay -q {}'.format(file_path))
        time.sleep(0.2)
