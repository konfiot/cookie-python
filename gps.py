import sys
import threading
import operator
import binascii
import serial
import functools

def coord(l, d):
	try:
		lin = float(l)
	except:
		lin = 0.0

	if d == "S" or d == "W":
		lin = -lin 

	degrees = int(lin/100)
	minutes = lin - degrees*100

	return degrees + (minutes/60)

def buildPMTK(data):
	return b"$" + data + b"*" + binascii.hexlify(bytearray([functools.reduce(operator.xor, data)])) + "\r\n"

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

class GPS(threading.Thread) :
	def __init__(self, port, speed):
		threading.Thread.__init__(self)
		self.ser = serial.Serial(port, 9600, dsrdtr=0)
		self.ser.write(buildPMTK(b"PMTK251," + bytearray(str(speed))))
		self.ser.close()
		self.ser = serial.Serial(port, speed, dsrdtr=0)

		self.ser.write(buildPMTK(bytearray("PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")))
		self.ser.write(buildPMTK(bytearray("PMTK220,100")))

		self.terminate = False
		self.finish_terminated = False

		self.out = [0]*4

	def stop(self):
		self.terminate = True
		while not self.finish_terminated: pass

	def run(self):
		while not self.terminate:
			buf = bytearray()
			while self.ser.read(1) != b"$": pass

			read = self.ser.read(1)

			while read != b"*":
				buf += read
				read = self.ser.read(1)

			try:
				cs = binascii.unhexlify(self.ser.read(2))
			except:
				continue

			csdata = bytearray([functools.reduce(operator.xor, buf)])

			data = str(buf.decode("ascii", errors="replace")).split(",")

			if cs == csdata: 
				if data[0] == "GPGGA":
					self.out[0] = int(coord(data[2], data[3]) * 1e7)
					self.out[1] = int(coord(data[4], data[5]) * 1e7)
					if isfloat(data[9]):
						self.out[2] = int(float(data[9]))
				elif data[0] == "GPRMC":
					self.out[0] = int(coord(data[3], data[4]) * 1e7)
					self.out[1] = int(coord(data[5], data[6]) * 1e7)
					if isfloat(data[7]):
						self.out[2] = int(float(data[7]) * 100)
				else:
					print("Trame non reconnue", data[0])
			else: 
				print("CS Fucked up")

		self.ser.close()
		self.finish_terminated = True


	def get_data(self):
		return self.out
