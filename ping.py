import sys
import threading
import time
import RPi.GPIO as GPIO

class Ping(threading.Thread) :
	def __init__(self, trigger_pin = 25, echo_pin = 24, size = 1.0):
		threading.Thread.__init__(self)

		self.terminate = False
		self.finish_terminated = False

		GPIO.setmode(GPIO.BCM)

		self.trigger_pin = trigger_pin
		self.echo_pin = echo_pin

		self.size = size

		self.out = [0]

		GPIO.setup(self.trigger_pin, GPIO.OUT)
		GPIO.setup(self.echo_pin, GPIO.IN)

		GPIO.output(self.trigger_pin, False)



	def stop(self):
		self.terminate = True
		while not self.finish_terminated: pass

	def run(self):
		while not self.terminate:
			failed = False

			time.sleep(.1)
			GPIO.output(self.trigger_pin, True)
			time.sleep(0.00001)
			GPIO.output(self.trigger_pin, False)

			timeout = time.time()

			while GPIO.input(self.echo_pin) == 0:
				start = time.time()
				if time.time() - timeout > .5:
					failed = True
					break

			timeout = time.time()

			while GPIO.input(self.echo_pin) == 1:
				stop = time.time()
				if time.time() - timeout > .5:
					failed = True
					break

			if not failed: 
				self.out[0] = int(10 * self.size / (stop - start))

		self.finish_terminated = True


	def get_data(self):
		return self.out
