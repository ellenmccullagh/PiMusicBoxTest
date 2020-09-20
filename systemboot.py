import buttonhandler as bh
#from threading import Thread
import RPi.GPIO as GPIO

class OnOffButton:
    def __init__(self, pin):
        self.pin = pin
        self.on = False

    def onoff(self):
        self.on = not(self.on)
        if self.on:
            bh.handleButtons()
        else:
            bh.signal_handler()

on_off_btn = OnOffButton(5)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(on_off_btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(on_off_btn.pin, GPIO.FALLING, on_off_btn.onoff, bouncetime=300)
