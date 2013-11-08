import logging

from .expression import Expression

BAUDRATE=9600
TIMEOUT=60

class ProtocolError(Exception): pass
class UnsupportedProtocolVersionError(ProtocolError): pass

class WandProtocol(object):
    def __init__(self, serial):
        self._serial = serial
        self._protocol_version = -1.0
        self._pixel_count = -1
        self._buffer = bytearray()

    def open(self):
        self._serial.open(baudrate=BAUDRATE, timeout=TIMEOUT, writeTimeout=TIMEOUT)

    def reset(self):
        self._write(b"RT")
        self._wait_response(b"RESET")
        self._write(b"xo")
        response = self._wait_response(b"OKv{f:version}")
        self._protocol_version = response.version

        response = self._wait_response(b"D{i:pixels}")
        self._pixel_count = response.pixels

    def width(self, w):
        self._write(b"W{0}".format(w))
        self._wait_response(b"OK")

    def send_batch(self, bytes):
        return self._write(bytes, with_newline=False)

    def _wait_response(self, bytes):
        e = Expression(bytes)
        data = self._readline()
        if not e(data):
            # TODO: Figure out what to do if we are invalid
            return None
        return e

    def _readline(self):
        found = False
        retval = bytearray()
        while not found:
            tmp = self._serial.read(100)
            idx = tmp.find(b'\n')
            if idx >= 0:
                found = True
                retval.extend(self._buffer)
                retval.extend(tmp[:idx])
                self._buffer = bytearray(tmp[idx+1:])
            else:
                self._buffer.extend(tmp)

        return retval

    @property
    def version(self):
        return self._protocol_version

    @property
    def pixels(self):
        return self._pixel_count


    def _write(self, bytes, with_newline=True):
        """ Writes a message followed by a new line character """
        tmp = bytearray(bytes)
        if with_newline:
            tmp.append(b'\n')
        retval = self._serial.write(tmp)
        logging.debug("Wrote {0} bytes".format(retval))
        return retval
