import RPi.GPIO as GPIO
import time
import signal
import sys
#from os import system, path
from mpd import MPDClient
from threading import Thread
import logging
#from systemd.journal import JournaldLogHandler
from systemd import journal

class Button(object):
    '''
       Buttons that correspond to playlists
    '''
    def __init__(self, pin, ledpin, color, playlist, uri = None):
        self.pin = pin
        self.color = color
        self.playlist = playlist
        self.uri = uri
        self.status = True #True means unpressed, False means pressed
        self.ledpin = ledpin
        LEDPINS.append(self.ledpin)
        GPIO.setup(self.ledpin, GPIO.OUT)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, self.playsound, bouncetime=1000)

    def updatelights(self):
        for pin in LEDPINS:
            GPIO.output(pin, 0)
        GPIO.output(self.ledpin, 1)


    def playsound(self, channel): #if the current playlist corresponds to this button, skip to the next track. Otherwise change the playlist and begin playback
        global currentplaylist
        log.info("Current playlist: {}".format(currentplaylist))
        #logging.info('The next song is number {}'.format(client.status()['nextsong']))
        if currentplaylist == self.playlist: #I am the current playlist
            client.next()
            log.info('{} next track'.format(self.playlist))
        else: #I am not the current playlist
            client.pause()
            client.clear()
            client.add(self.uri)
            client.play()
            log.info('{} playing'.format(self.playlist))
            currentplaylist = self.playlist
            self.updatelights()
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



def stopcallback(channel):
    if client.status()['state'] == 'play': #playlist is already playing
        client.pause()
        log.info('Paused')
    elif client.status()['state'] == 'pause': #playlist is paused
        client.play()
        log.info('Resumed')

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
    #logging.basicConfig(level=logging.DEBUG, filename='playpausetest.log', filemode='w')


    log = logging.getLogger('demo')
    log.addHandler(journal.JournaldLogHandler())
    log.setLevel(logging.DEBUG)
    log.info("sent to journal")
    # logger = logging.getLogger('buttonhandler')
    # journald_handler = JournaldLogHandler()
    # journald_handler.setFormatter(logging.Formatter( '[%(levelname)s] %(message)s'))
    # logger.addHandler(journald_handler)
    # logging.info('Logging established')

    global client
    client = MPDClient()
    #time.sleep(180)
    for i in range(10):
        try:
            client.connect("localhost", 6600)
            log.debug('Connected!')
            #system('aplay -q {}'.format('~/projects/PiMusicBoxTest/sounds/tada.wav'))
            break
        except:
            log.debug('{} try connection failed.'.format(i+1))
            time.sleep(30)


    global LEDPINS
    LEDPINS = []

    GPIO.setmode(GPIO.BCM)
    currentplaylist = 'None'

    #ping client to maintain connection
    client.setvol(60)
    global pinging
    pinging = Thread(target=clientPing)
    pinging.start()

    #Declare all buttons
    BUTTON_PINS = [
                    Button(5, 23, 'Blue', 'Both Frozens', 'spotify:playlist:6gBXZmySP7a6n4PZJhaqYO'),
                    Button(13, 25, 'Green', 'Miles favorites', 'spotify:playlist:1eKf1Q2I7GKi3BfHTNL4Dt'),
                    Button(16, 22, 'Yellow', 'Lullabies for Miles', 'spotify:playlist:22xETQTI3B6RzEdgBqPqXS'),
                    Button(6, 24, 'White', 'Listen and Play Podcast', 'spotify:show:6NEs2aWiXSmXWoTRFh8fUN') #playtime for miles: spotify:playlist:3pByZu2SyYiNlIppLXbUZ7
                    ]

    #playpause button
    STOP_BUTTON = 12

    #setup playback buttons
    #for btn in BUTTON_PINS:


    #setup stop button
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(STOP_BUTTON, GPIO.BOTH, stopcallback, bouncetime=1000)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
