import ..trame
import argparse

parser = argparse.ArgumentParser(description='Generates a random trame')
parser.add_argument('length', metavar='N', type=int, nargs='1', help='Number of sensors')
parser.add_argument('type', type=int, nargs='1', help='type of sensor value (struct.pack compatible)')
parser.add_argument('ecclength', type=int, nargs='1', help='length of the reed-solomon error correcting code')
parser.add_argument('--startbyte', dest=startbyte, default=0xFF, type=int, help='Start byte (defaults to 0xFF)')

