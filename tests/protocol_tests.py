from unittest import TestCase
import _helpers as h

from pwl.protocol import WandProtocol

class ProtocolTests(TestCase):
    def test_reset(self):
        mock = h.MockSerial(
            [
                'RT',
                'xo'
             ],
            [
                'RST',
                'OKv1.0',
                'D25'
            ]
        )
        uut = WandProtocol(mock)
        uut.open()
        uut.reset()
        self.assertAlmostEqual(uut.version, 1.0)
        self.assertEqual(uut.pixels, 25)

    def test_width_set(self):
        mock = h.MockSerial(
            [
                "W25"
            ],
            [
                "OK"
            ]
        )

        uut = WandProtocol(mock)
        uut.open()
        uut.width(25)
