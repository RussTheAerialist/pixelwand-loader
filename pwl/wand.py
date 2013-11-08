import logging

from .protocol import WandProtocol

class Wand(object):
    def __init__(self, serial):
        self._protocol = WandProtocol(serial)
        self._number_pixels = -1
        self._width = -1

    def start_upload(self):
        self._open()

        self._protocol.reset()
        version = self._protocol.version
        logging.info("Wand Version {0} connected".format(version))


        self._number_pixels = response.pixels
        logging.info("{0} pixels present".format(self._number_pixels))

    def number_pixels(self):
        return self._number_pixels

    def set_width(self, width):
        self._width = width
        self._write(b"W{0}".format(width))

    def send_bytes(self, bytes):
        while self.send_batch(bytes, self._number_pixels) > 0: pass

    def send_batch(self, gen, num):
        try:
            arr = bytearray()
            for i in range(num):
                arr.extend(gen.next())
            self._write(arr)
            return 1
        except StopIteration:
            return 0

    def _open(self):
        self._protocol.open()

class MockWand(Wand):
    def _generate_responses(self):
        yield b"RESET"
        yield b"OKv1.0"
        yield b"D25"

    def __init__(self, serial):
        super(MockWand, self).__init__(serial)
        self._responses = self._generate_responses()

    def _open(self):
        pass

    def _close(self):
        pass

    def _write(self, bytes):
        logging.debug(bytes)
        pass

    def _read(self):
        return self._responses.next()
