import RPi.GPIO as GPIO
import time

import signal
import sys
from os import system, path

#BUTTON_GPIO = 16
class Button(object):
    '''
       Buttons. What they look like, what they do, where they are etc.
    '''
    def __init__(self, pin, color, sound):
        self.pin = pin
        self.color = color
        self.sound = sound
        self.basepath = '~/projects/PiMusicBoxTest/'
        self.status = True

    def playsound(self):
        system('aplay -q {}'.format(base_path + self.sound + '.wav'))
        pass

    def updateStatus(self):
        self.status = GPIO.input(self.pin)
        pass

    def reportStatus(self):
        return self.status

    def reportColor(self):
        return self.color

BUTTON_PINS = [
                Button(5, 'Red', 'moo'),
                Button(5, 'Blue', 'tada'),
                Button(12, 'Green', 'Tada'),
                Button(13, 'Yellow', 'rooster'),
                Button(16, 'White', 'tada')
                ]
                # {
                # 5: 'moo', #Red
                # 6: 'tada', #Blue
                # 12: 'tada', #Green
                # 13: 'rooster', #Yellow
                # 16: 'tada' #White
                # }

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    for btn in BUTTON_PINS:
        btn.updateStatus()
        if btn.reportStatus() == False:
            btn.playsound()
            print("{} button pressed".format(self.reportColor()))
            break
        # if GPIO.input(pin) == False:
        #     system('aplay -q {}'.format(base_path + BUTTON_PINS[pin] + '.wav'))
        #     print("Button {} pressed!".format(pin))
        #     break

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    for btn in BUTTON_PINS:
        GPIO.setup(btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for btn in BUTTON_PINS:
        GPIO.add_event_detect(btn.pin, GPIO.FALLING,
            callback=btn.playsound, bouncetime=50)  #button_pressed_callback

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
