import logging

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


    @property
    def version(self):
        return self._protocol_version

    @property
    def pixels(self):
        return self._pixel_count


    def _write(self, bytes):
        """ Writes a message followed by a new line character """
        tmp = bytearray(bytes)
        logging.debug(bytes)
        tmp.append(b'\n')
        logging.debug("Wrote {0} bytes".format(
            self._serial.write(bytes)
        ))