import logging
import time

import serial

from .expression import Expression

BAUDRATE=9600
TIMEOUT=60

class ProtocolError(Exception): pass
class UnsupportedProtocolVersionError(ProtocolError): pass

class WandProtocol(object):
    def __init__(self, s, full_reset):
        self._full_reset = full_reset
        self._serial = serial.Serial()
        self._serial.port = s
        self._protocol_version = -1.0
        self._pixel_count = -1
        self._buffer = bytearray()

    def open(self):
        self._serial.baudrate=BAUDRATE
        self._serial.timeout=TIMEOUT
        self._serial.writeTimeout=TIMEOUT
        self._serial.open()
        self._serial.flushOutput()
        self._serial.flushInput()

    def reset(self):
        if self._full_reset:
            self._write(b"RT")
            self._wait_response(b"RST")
        logging.debug(self._write(b"xo"))
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
        logging.debug("Waiting for: {0}".format(bytes))
        e = Expression(bytes)
        data = self._readline()
        logging.debug("Line:{0}".format(data))
        if not e(data):
            # TODO: Figure out what to do if we are invalid
            return None
        return e

    def _readline(self):
        logging.debug("Starting Readline with: {0}".format(self._buffer))
        found = False
        retval = bytearray()
        while not found:
            waiting_chars = self._serial.inWaiting()
            logging.debug("{0} waiting".format(waiting_chars))
            if waiting_chars > 0:
                tmp = self._serial.read(1)
                logging.debug("read:'{0}'".format(tmp))
                logging.debug("buffer = {0}".format(self._buffer))
                idx = tmp.find(b'\n')
                if idx >= 0:
                    found = True
                    retval.extend(self._buffer)
                    retval.extend(tmp[:idx])
                    self._buffer = bytearray(tmp[idx+1:])
                else:
                    self._buffer.extend(tmp)
            else:
                time.sleep(0.1)

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
        self._serial.flush()
        time.sleep(0.1)  # http://stackoverflow.com/questions/7266558/pyserial-buffer-wont-flush
        return retval
