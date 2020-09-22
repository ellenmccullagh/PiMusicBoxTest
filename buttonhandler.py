import RPi.GPIO as GPIO
import time
import signal
import sys
#from os import system, path
from mpd import MPDClient
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG, filename='playpausetest.log', filemode='w')

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
        logging.info("Current playlist: {}".format(currentplaylist))
        print('The next song is number {}'.format(client.status()['nextsong']))
        if currentplaylist == self.playlist:
            client.next()
            logging.info('{} next track'.format(self.playlist))
        else:
            client.pause()
            client.clear()
            client.add(self.uri)
            client.play()
            logging.info('{} playing'.format(self.playlist))
            currentplaylist = self.playlist
        pass

    def seturi(self, uri):
        self.uri = uri
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
                Button(6, 'Blue', 'Both Frozens', 'spotify:playlist:6gBXZmySP7a6n4PZJhaqYO'),
                Button(12, 'Green', 'Miles favorites', 'spotify:playlist:1eKf1Q2I7GKi3BfHTNL4Dt'),
                Button(13, 'Yellow', 'Lullabies for Miles', 'spotify:playlist:22xETQTI3B6RzEdgBqPqXS'),
                Button(16, 'White', 'Playtime for Miles', 'spotify:playlist:3pByZu2SyYiNlIppLXbUZ7')
                ]

'''
Declare pause/resume toggle button pin and callback function
'''
STOP_BUTTON = 5

def stopcallback(channel):
    if client.status()['state'] == 'play': #playlist is already playing
        client.pause()
        logging.info('Paused')
    elif client.status()['state'] == 'pause': #playlist is paused
        client.play()
        logging.info('Resumed')

def clientPing(): #avoid client disconnect by pinging regularly.
    while True:
        client.ping()
        time.sleep(10)

def signal_handler(sig, frame): #used to close and cleanup GPIO and mopidy mdp client
    GPIO.cleanup()
    client.pause()
    client.close()
    client.disconnect()
    pinging.join()
    sys.exit(0)

if __name__ == '__main__':

    global client
    client = MPDClient()
    for i in range(4):
        time.sleep(30)
        try:
            client.connect("localhost", 6600)
            logging.debug('Connected!')
            #system('aplay -q {}'.format('~/projects/PiMusicBoxTest/sounds/tada.wav'))
            break
        except:
            logging.debug('{} try connection failed.'.format(i+1))

    client.setvol(60)
    global pinging
    pinging = Thread(target=clientPing)
    pinging.start()

    GPIO.setmode(GPIO.BCM)

    currentplaylist = 'None'

    #setup playback buttons
    for btn in BUTTON_PINS:
        GPIO.setup(btn.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn.pin, GPIO.FALLING, btn.playsound, bouncetime=300)

    #setup stop button
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(STOP_BUTTON, GPIO.RISING, stopcallback, bouncetime=300)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
