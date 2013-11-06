import logging

class ProtocolError(Exception): pass

class Wand(object):
    def __init__(self, serial):
        self._number_pixels = -1
        self._width = -1

    def start_upload(self):
        # self.serial.open()
        self._write(b"xo")
        bytes = self._read()

        if bytes[:2] != b"OK":
            raise ProtocolError("Wand Not Responding")
        if bytes[2] != b"v":
            raise ProtocolError("Wand did not provide protocol version")

        version = float(bytes[3:])
        if version < 1.0:
            raise ProtocolError("Incompatible version of wand: {0}".format(version))
        logging.info("Wand Version {0} connected".format(version))

        bytes = self._read()
        if bytes[0] != b"D":
            raise ProtocolError("Next Response should be D## for pixel count")
        self._number_pixels = int(bytes[1:])
        logging.info("{0} pixels present".format(self._number_pixels))

    def number_pixels(self):
        return self._number_pixels

    def set_width(self, width):
        self._width = width
        self._write(b"W{0}".format(width))

class MockWand(Wand):
    def _generate_responses(self):
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
        pass

    def send_bytes(self, bytes):
        pass

    def _read(self):
        return self._responses.next()
