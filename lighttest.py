import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Pins = {
'blue button light':25,
'yellow button light': 24,
'green button light': 23,
'white button light': 22,
'side leds': 21
}

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

for pin in pins:
    GPIO.output(pin, 1)
    time.sleep(1)
    GPIO.output(pin, 0)
