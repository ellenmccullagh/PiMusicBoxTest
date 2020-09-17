import RPi.GPIO as GPIO
import time

import signal
import sys

#BUTTON_GPIO = 16
BUTTON_PINS = {
                5: 'moo', #Red
                6: 'tada', #Blue
                12: 'tada', #Green
                13: 'rooster', #Yellow
                16: 'tada' #White
                }
base_path = '~/projects/PiMusicBoxTest/'

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    for pin in BUTTON_PINS:
        if GPIO.input(pin) == False:
            system('aplay -q {}'.format(file_path_moo + BUTTON_PINS[pin] + '.wav'))
            print("Button {} pressed!".format(pin))
            break

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    for pin in BUTTON_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        for pin in BUTTON_PINS:
            GPIO.add_event_detect(pin, GPIO.FALLING,
                callback=button_pressed_callback, bouncetime=100) #i'm not sure how to pass the pin number to the callback function. Maybe I need to embed this in a class somehow

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

#
# GPIO.setmode(GPIO.BCM)
# from os import path, system
#
#
#
# file_path_tada = '~/projects/PiMusicBoxTest/tada.wav'
# file_path_moo = '~/projects/PiMusicBoxTest/moo.wav'
# file_path_rooster = '~/projects/PiMusicBoxTest/rooster.wav'
#
#
# for pin in BUTTON_PINS:
#         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
# while True:
#         input_states = [(BUTTON_PINS[pin], GPIO.input(pin)) for pin in BUTTON_PINS]
#         playback = threading.Thread(target=playback_thread, args=(1,), daemon = True)
#
#         for state in input_states:
#                 if state[1] == False:
#                         print('Button {} Pressed'.format(state[0]))
#                         if state[0] == 'Red':
#                             system('aplay -q {}'.format(file_path_moo))
#                         elif state[0] == 'Yellow':
#                             system('aplay -q {}'.format(file_path_rooster))
#                         else:
#                             system('aplay -q {}'.format(file_path_tada))
#         time.sleep(0.2)
