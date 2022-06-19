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
    mp3 = 'http://www.hyperion-records.co.uk/audiotest/3%20Schubert%20String%20Quartet%20No%2014%20in%20D%20minor%20Death%20and%20the%20Maiden,%20D810%20-%20Movement%203%20Scherzo%20Allegro%20molto.MP3'
    
    try:
        client.connect("localhost", 6600)
        log.info('Established connection')
    except:
        log.info('Connection failed (1)')

    client.pause()
    client.clear()
    client.add(currentplaylist)
    client.next()
    client.play()
    

if __name__ == '__main__':
    main()