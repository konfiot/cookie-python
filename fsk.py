# coding=utf-8

import math
import itertools
import sys
import audiogen
import threading
import trame

MARK_HZ = 900.0
SPACE_HZ = 1500.0
BAUD_RATE = 600.0

TWO_PI = 2.0 * math.pi
class Fsk(threading.Thread) :
    def __init__(self, conf, initial_data = b""):
        threading.Thread.__init__(self)
        self.to_send = initial_data
        self.conf = conf

    def encode(self, data):
        for sample in itertools.chain.from_iterable([self.modulatebyte(c) for c in data]):
            yield sample

    def modulatebyte(self, byte):
        #print byte
        seconds_per_sample = 1.0 / audiogen.sampler.FRAME_RATE
        phase, seconds, bits = 0, 0, 0

        clock = (x / BAUD_RATE for x in itertools.count(1))
        tones = (SPACE_HZ if i == 0 or not((byte >> (i-1)) & 1) and i <= 8 else MARK_HZ for i in range(10))

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
            # print int(frequency == MARK_HZ)

    def feed(self, data):
        self.to_send = trame.trame(data, conf)

    def run(self):
        self.terminate = False
        while not self.terminate:
            audiogen.sampler.write_wav(sys.stdout, self.encode(self.to_send))

    def stop(self):
        self.terminate = True

