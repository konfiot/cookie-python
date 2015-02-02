#!/usr/bin/python3
import trame
import argparse
import json
import struct
import os
import sys
import time

parser = argparse.ArgumentParser(description='Generates a random trame')
parser.add_argument('--length', type=int, default=5, help='Number of sensors (defaults to 5)')
parser.add_argument('--type', type=str, default='i', help='type of sensor value (struct.pack compatible) (defaults to \'i\')')
parser.add_argument('--ecclength', default=10, type=int, help='length of the reed-solomon error correcting code (defaults to 10)')
parser.add_argument('--startbyte', default=0xFF, type=int, help='Start byte (defaults to 0xFF)')
parser.add_argument('--file', type=str, help='Input config file')
parser.add_argument('--out', default=sys.stdout.buffer, type=argparse.FileType('wb'), help='Output file (defaults to stdout)')
parser.add_argument('-N', type=int, default=-1, help='Number of frames to be generated (defaults to infinite)')
parser.add_argument('-t', type=int, default=1, help='Time between two frames (defaults to 1s)')
args = parser.parse_args()

if args.file :
    conf = json.load(open(args.file, "r"))
else :
    conf = {"sensors": [args.valtype]*args.length, "trame":{"startbyte": args.startbyte, "ecc":{"length":args.ecclength}}}

N = args.N
while N != 0:
	args.out.write(trame.trame(struct.unpack(''.join(conf["sensors"]), os.urandom(struct.calcsize(''.join(conf["sensors"])))), conf))
	N -= 1
	args.out.flush()
	time.sleep(args.t)

