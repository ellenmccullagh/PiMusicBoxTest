import RPi.GPIO as GPIO
import time
import signal
import sys
from mpd import MPDClient
from threading import Thread
import logging
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


    def playsound(self, channel):
        '''
        If the current playlist corresponds to this button, skip to the next track.
        Otherwise change the playlist and begin playback
        '''

        global currentplaylist
        log.info("Current playlist: {}".format(currentplaylist))

        #Check mopidy connection and reconnect if disconnected
        try:
            client.ping()
            log.info("Already connected")
        except:
            try:
                client.connect("localhost", 6600)
                log.info("Reestablished connection")
            except:
                log.info("Connection failed (2)")

        client.setvol(60)

        if currentplaylist == self.playlist: #I am the current playlist
            client.next()
            log.info('{} next track'.format(self.playlist))
        else: #I am not the current playlist
            client.pause()
            client.clear()
            client.add(self.uri)
            time.sleep(0.1)
            client.play()
            log.info('{} playing'.format(self.playlist))
            currentplaylist = self.playlist
            self.updatelights()

        client.disconnect()
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
    #check connection
    try:
        client.ping()
        log.info("Already connected")
    except:
        try:
            client.connect("localhost", 6600)
            log.info("Reestablished connection (3)")
        except:
            log.info("Connection failed (3)")

    #play pause
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
    #pinging.join()
    sys.exit(0)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG, filename='playpausetest.log', filemode='w')


    log = logging.getLogger('musicbox')
    log.addHandler(journal.JournaldLogHandler())
    log.setLevel(logging.DEBUG)
    log.info("sent to journal")

    global client
    client = MPDClient()

    #time.sleep(180)
    # for i in range(10):
    #     try:
    #         client.connect("localhost", 6600)
    #         log.debug('Connected!')
    #         #system('aplay -q {}'.format('~/projects/PiMusicBoxTest/sounds/tada.wav'))
    #         break
    #     except:
    #         log.debug('{} try connection failed.'.format(i+1))
    #         time.sleep(30)


    global LEDPINS
    LEDPINS = []

    GPIO.setmode(GPIO.BCM)
    currentplaylist = 'None'

    #ping client to maintain connection

    # global pinging
    # pinging = Thread(target=clientPing)
    # pinging.start()


    #playpause button
    STOP_BUTTON = 12

    #Wait until red button is pushed to start connection etc.
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
        time.sleep(0.1)
    log.info('Begin connection')

    #connect to mopidy using mpd client
    try:
        client.connect("localhost", 6600)
        log.info('Established connection')
    except:
        log.info('Connection failed (1)')

    #setup stop button
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(STOP_BUTTON, GPIO.BOTH, stopcallback, bouncetime=1000)

    #Declare all playlist buttons. GPIO event established in object init
    BUTTON_PINS = [
                    Button(5, 23, 'Blue', 'Both Frozens', 'spotify:playlist:6gBXZmySP7a6n4PZJhaqYO'),
                    Button(13, 25, 'Green', 'Miles favorites', 'spotify:playlist:1eKf1Q2I7GKi3BfHTNL4Dt'),
                    Button(16, 22, 'Yellow', 'Lullabies for Miles', 'spotify:playlist:22xETQTI3B6RzEdgBqPqXS'),
                    Button(6, 24, 'White', 'Stories', 'https://dts.podtrac.com/redirect.mp3/traffic.megaphone.fm/BUR2983452505.mp3')
                    #spotify:playlist:0C7SxyofEe3bAWqxmyhruA' )#'spotify:playlist:7yYG0ULqH3D2NXiCG3HBOE') #playtime for miles: spotify:playlist:3pByZu2SyYiNlIppLXbUZ7 old stories playlist: spotify:playlist:0IJH6tPwq2lns377i4YvMd
                    ]


    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
