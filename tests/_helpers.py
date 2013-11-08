import unittest

class ExpectedValueFailure(AssertionError): pass

class MockSerial(object):
    def __init__(self, inputs, outputs):
        self._inputs = inputs
        self._outputs = outputs
        self._open_called = False

    def open(self, *args, **kargs):
        self._open_called = True

    def read(self, length):
        assert self._open_called, "read called before open"

        output = bytearray(self._outputs.pop(0))  # Take the first item
        output.extend(b'\n')

        return output

    def write(self, bytes):
        assert self._open_called, "write called before open"

        expected = self._inputs.pop(0)
        if len(expected) != len(bytes) or expected != bytes:
            raise ExpectedValueFailure("'{0}'!='{1}'".format(expected, bytes))

        return len(bytes)
