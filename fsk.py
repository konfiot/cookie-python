# coding=utf-8

# Bell 202 Audio Frequency Shift Keying
# http://n1vg.net/packet/

import logging
logger = logging.getLogger(__name__)

import math
import itertools
import sys
import audiogen

MARK_HZ = 900.0
SPACE_HZ = 1500.0
BAUD_RATE = 600.0

TWO_PI = 2.0 * math.pi

def encode(data):
	for sample in itertools.chain.from_iterable([modulatebyte(c) for c in data]):
		yield sample

def modulatebyte(byte):
	#print byte
	seconds_per_sample = 1.0 / audiogen.sampler.FRAME_RATE
	phase, seconds, bits = 0, 0, 0

	# construct generators
	clock = (x / BAUD_RATE for x in itertools.count(1))
	tones = (SPACE_HZ if i == 0 or not((ord(byte) >> (i-1)) & 1) and i <= 8 else MARK_HZ for i in range(10))

	for boundary, frequency in itertools.izip(clock, tones):
		# frequency of current symbol is determined by how much
		# we advance the signal's phase in each audio frame
		phase_change_per_sample = TWO_PI / (audiogen.sampler.FRAME_RATE / frequency)

		# produce samples for the current symbol
		# until we reach the next clock boundary
		while seconds < boundary:
			yield math.sin(phase)

			seconds += seconds_per_sample
			phase += phase_change_per_sample

			if phase > TWO_PI:
				phase -= TWO_PI

		bits += 1
		#print int(frequency == MARK_HZ)
		#print("bits = %d, time = %.7f ms, expected time = %.7f ms, error = %.7f ms, baud rate = %.6f Hz" \
		#	% (bits, 1000 * seconds, 1000 * bits / BAUD_RATE, 1000 * (seconds - bits / BAUD_RATE), bits / seconds))

audiogen.sampler.write_wav(sys.stdout, encode(b"Dandandan"))
