#!/usr/bin/env python
import time
import max7219.led as led
import max7219.font as font
import mpd
import symbols
from socket import error as socket_error
#import errno

# debugging output
import logging, mpd
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)
import sys
print(sys.version)

print('connecting devices...')

### connect to LED matrix
#device = led.matrix()				# when using only one matrix
device = led.matrix(cascaded=2)
#device.brightness(15)
device.orientation(180)

### connect to MPD
client = mpd.MPDClient()               # create client object
host="localhost"
port=6600
client.timeout = 10                # network timeout in seconds (floats allowed), default: None

notConnected = True
while notConnected:
	try:
		client.connect(host, port)
		print('connected.')
		notConnected = False
	except socket_error:
		time.sleep(1)
		print('retry...')

#print(client.mpd_version)

symbols.plot_matrix(device, symbols.smiley)

while True:
	client.idle()

	status = client.status()	# Reports the current status of the player and the volume level.
	if status['state'] == 'play':
		symbols.plot_matrix(device, symbols.play)
		device.brightness(10)
		time.sleep(0.5)

		currentsong = client.currentsong()
		artist = currentsong.get('albumartist', 'NoArtist')	# get, if not exist else
		title = currentsong.get('title', 'NoTitle')
		message = artist + ' - ' + title
#		album = currentsong['album']
#		message = artist + ' - ' + album + ' - ' + title

		device.show_message(message, font=font.LCD_FONT) #SINCLAIR_FONT

		symbols.plot_matrix(device, symbols.play)
	else:
		if status['state'] == 'pause':
			symbols.plot_matrix(device, symbols.pause)
		else:
			symbols.plot_matrix(device, symbols.stop)
		device.brightness(5)

client.close()                     # send the close command
client.disconnect()                # disconnect from the server


