import logging
import sys
import argparse

from .wand import Wand, MockWand
from .loader import Loader

def parse_args(args):
    parser = argparse.ArgumentParser(description="Load an image into the PixelWand")
    parser.add_argument("-n", action="store_true", help="Emulate the Wand")
    parser.add_argument("-v", action="store_const", default=logging.INFO, const=logging.DEBUG, help="Verbose")
    parser.add_argument("-r", action="store_true", help="reset the device before loading")
    parser.add_argument("-s", action="store_true", help="slow start for nano")
    parser.add_argument("serial", help="path to the serial device")
    parser.add_argument("png", help="path to the png file to load")

    options = parser.parse_args(args)
    logging.basicConfig(level=options.v)

    return options

def main(args=sys.argv[1:]):
    options = parse_args(args)
    if options.n:
        wand = MockWand(options.serial)
    else:
        wand = Wand(options.serial, options.r, options.s)
    loader = Loader(options.png)

    loader.send_to(wand)

if __name__ == "__main__":

    main()
