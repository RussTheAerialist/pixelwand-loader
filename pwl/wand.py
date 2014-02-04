import logging
import time

from .protocol import WandProtocol

class Wand(object):
    def __init__(self, serial, do_full_reset=False, slow_start=False):
        self._protocol = WandProtocol(serial, do_full_reset)
        self._number_pixels = -1
        self._width = -1
        self._slow_start = slow_start

    def start_upload(self):
        self._open()
        if self._slow_start:
            time.sleep(2)

        self._protocol.reset()
        version = self._protocol.version
        logging.info("Wand Version {0} connected".format(version))

        self._number_pixels = self._protocol.pixels
        logging.info("{0} pixels present".format(self._number_pixels))

    def number_pixels(self):
        return self._number_pixels

    def set_width(self, width):
        logging.info("Setting upload width to {0}".format(width))
        self._protocol.width(width)

    def send_bytes(self, bytes):
        sends = list(self.send_batch(bytes, self._number_pixels))
        total_bytes = sum(sends)
        logging.info("Total Image Upload Size: {0}+1".format(total_bytes))
 
    def send_batch(self, gen, num):
        while True:
            arr = bytearray()
            for i in range(num):
                    arr.extend(gen.next())
            retval = self._protocol.send_batch(arr)
            logging.debug("send_batch = {0}".format(retval))
            yield retval

    def _open(self):
        self._protocol.open()

class MockWand(Wand):
    def _generate_responses(self):
        yield b"RST"
        yield b"OKv1.0"
        yield b"D25"
        yield b"OK"

    class MockSerial(object):
        def __init__(self, parent): self._parent = parent
        def open(self, *args, **kargs): pass
        def write(self, bytes):
            return len(bytes)

        def read(self, length):
            try:
                retval = self._parent._responses.next()
                logging.debug("Read '{0}'".format(retval))
                return retval + b"\n"
            except StopIteration:
                return ""

    def __init__(self, serial):
        super(MockWand, self).__init__(MockWand.MockSerial(self))
        self._responses = self._generate_responses()
