#!/usr/bin/python2

from fsk import Fsk
import struct
import json 
import time
import os
import spidev
from gps import GPS


NUMBER_ANALOG = 8

spi = spidev.SpiDev()
spi.open(0,0)


def readChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data >> 2

def getAnalog(n):
	return [readChannel(i) for i in range(n)]

def getGPS():
	pass

def getIMU():
	pass

def getPing():
	pass

with open("conf.json") as fconf, open("dump.txt", "a") as fdump:
	conf = json.load(fconf)
	fsk = Fsk(conf)
	fsk.start()

	gps = GPS("/dev/ttyS3", 38400)
	gps.start()

	while True:
		vals = []
		vals.append(getAnalog(NUMBER_ANALOG))
		vals.append(gps.get_data())
		#vals.append(getPing())
		
		#for fmt in conf["sensors"]:
		#	val = struct.unpack("!" + fmt, os.urandom(struct.calcsize(''.join(fmt))))
		#	vals.append(val)

		fsk.feed(vals)
		fdump.write(",".join(map(str, vals)))
		time.sleep(0.1)
