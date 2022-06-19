import time
import signal
import sys
from mpd import MPDClient
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('musicbox')

log.info("Starting Mopidy Test")
client = MPDClient()

