from fsk import Fsk
import struct
import json 
import time
import os
import spidev

NUMBER_ANALOG = 8


def getChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def getAnalog(n):
	return [readCHannel(i) for i in range(n)]

def getGPS():
	pass

def getIMU():
	pass

def getPing():
	pass

with open("conf.json") as f:
	conf = json.load(f)
	vals = []
	fsk = Fsk(conf)
	fsk.start()
	while True:
		vals.append(getAnalog(NUMBER_ANALOG))
		vals.append(getGPS())
		vals.append(getPing())
		

		#for fmt in conf["sensors"]:
		#	val = struct.unpack("!" + fmt, os.urandom(struct.calcsize(''.join(fmt))))
		#	vals.append(val)

		fsk.feed(struct.unpack(''.join(conf["sensors"]), vals))
		time.sleep(0.5)
