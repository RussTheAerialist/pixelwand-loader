import logging
import sys
import argparse

from .wand import Wand, MockWand
from .loader import Loader

def parse_args(args):
    parser = argparse.ArgumentParser(description="Load an image into the PixelWand")
    parser.add_argument("-n", action="store_true", help="Emulate the Wand")
    parser.add_argument("serial", help="path to the serial device")
    parser.add_argument("png", help="path to the png file to load")

    return parser.parse_args(args)

def main(args=sys.argv[1:]):
    options = parse_args(args)
    if options.n:
        wand = MockWand(options.serial)
    else:
        wand = Wand(options.serial)
    loader = Loader(options.png)

    loader.send_to(wand)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
