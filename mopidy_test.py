import time
import signal
import sys
from mpd import MPDClient
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('musicbox')

log.info("Starting Mopidy Test")

#connect to mopidy using mpd client
def main():
    client = MPDClient()

    currentplaylist = 'https://soundcloud.com/discover/sets/track-stations:1080912754'
    client.add(currentplaylist)
    client.next()
    client.play()
    
    try:
        client.connect("localhost", 6600)
        log.info('Established connection')
    except:
        log.info('Connection failed (1)')

if __name__ == '__main__':
    main()