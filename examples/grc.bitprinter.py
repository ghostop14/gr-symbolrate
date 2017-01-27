#!/usr/bin/python

from __future__ import print_function
from functools import partial
import sys,getopt,os.path

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main(argv):
    filename=''

    if len(sys.argv) < 2:
        print('Usage: grc.bitprinter.py -i <inputfile>')
        print('bitprinter is meant to work with the output of the gnuradio binary slicer.')
        print('bitprinter will read each byte from <inputfile> where each byte represents a bit, and print it as a 0 or 1, or 2 or 3 if its a marker.')
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('Usage: grc.bitprinter.py -i <inputfile>')
        print('bitprinter is meant to work with the output of the gnuradio binary slicer.')
        print('bitprinter will read each byte from <inputfile> where each byte represents a bit, and print it as a 0 or 1, or 2 or 3 if its a marker.')
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: grc.bitprinter.py -i <inputfile>')
            print('bitprinter is meant to work with the output of the gnuradio binary slicer.')
            print('bitprinter will read each byte from <inputfile> where each byte represents a bit, and print it as a 0 or 1, or 2 or 3 if its a marker.')
            sys.exit()
        elif opt in ("-i","--ifile"):
            filename=arg

    if len(filename) == 0:
        print ("Error: please provide an input file.")
        sys.exit(2)

    if not os.path.isfile(filename):
        print ("Error: '", filename, "' does not exist.")
        sys.exit(2)

    eprint('Processing ', filename,"\n")

    with open(filename, 'rb') as file:
        for byte in iter(partial(file.read, 1), b''):
            # Do stuff with byte
            ord_byte=ord(byte)

            if ord_byte== 0:
                print('0',end="")
            elif ord_byte== 1:
                print('1',end="")
            elif ord_byte== 2:
                print('')
                print('0',end="")
            elif ord_byte== 3:
                print('')
                print('1',end="")

    print('')
    eprint("Done.\n")

if __name__ == "__main__":
    main(sys.argv[1:])

