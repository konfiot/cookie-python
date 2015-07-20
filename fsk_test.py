from fsk import Fsk
import struct
import json 
import time
import os

with open("conf.json") as f:
	conf = json.load(f)
	fsk = Fsk(conf)
	fsk.start()
	while True:
		fsk.feed(struct.unpack(''.join(conf["sensors"]), os.urandom(struct.calcsize(''.join(conf["sensors"])))))
		time.sleep(0.5)
