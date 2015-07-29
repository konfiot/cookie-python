import sys
import time
import threading
import smbus

def signed(i):
	return (i + 2**15) % 2**16 - 2**15

class IMU(threading.Thread) :
	def __init__(self, imu_address, mag_address):
		threading.Thread.__init__(self)

		self.bus = smbus.SMBus(2)

		self.imu_address = imu_address
		self.mag_address = mag_address

		b = self.bus.read_byte_data(self.imu_address, 0x6B)
		b ^= (1 << 6)
		self.bus.write_byte_data(self.imu_address, 0x6B, b)
		self.terminate = False

		self.finish_terminated = False

		self.out = [0]*10

	def stop(self):
		self.terminate = True
		while not self.finish_terminated: pass

	def run(self):
		while not self.terminate:
			self.bus.write_byte_data(self.imu_address, 0x1C, 0b00001000)
			time.sleep(.02)
			self.bus.write_byte_data(self.imu_address, 0x1B, 0b00001000)
			time.sleep(.02)

			out = [signed(self.bus.read_word_data(self.imu_address, 2*n + 0x3B)) for n in range(7)]

			self.bus.write_byte_data(self.imu_address, 0x37, 0x02)
			time.sleep(0.01)
			self.bus.write_byte_data(self.mag_address, 0x0A, 0x01)
			time.sleep(0.01)

			out += [signed(self.bus.read_word_data(self.mag_address, 2*n + 0x03)) for n in range(3)]
			
			self.out = out
			

		self.finish_terminated = True


	def get_data(self):
		return self.out
