from unittest import TestCase

from pwl.expression import Expression

class ExpressionTest(TestCase):
    def test_literals_only_valid(self):
        uut = Expression("THANKS")
        uut("THANKS12345")
        self.assert_(uut.valid)
        self.assertEqual(uut.leftover, "12345")

    def test_literals_only_pretext(self):
        uut = Expression("THANKS")
        self.assert_(not uut("XOTHANKS1234"))
        self.assertEqual(uut.leftover, "XOTHANKS1234")

    def test_variable_string(self):
        uut = Expression("OKd{s:filename}")
        self.assert_(uut("OKdtest.png"))
        self.assertEqual(uut.filename, "test.png")

    def test_variable_int(self):
        uut = Expression("OKv{i:version}")
        self.assert_(uut("OKv1"))
        self.assertEqual(uut.version, 1)

    def test_variable_int_invalid(self):
        uut = Expression("OKv{i:version}")
        self.assert_(not uut("OKvBAM"))
        self.assert_(not getattr(uut, "version", False))

    def test_variable_float(self):
        uut = Expression("OKv{f:version}")
        self.assert_(uut("OKv1.1"))
        self.assertAlmostEqual(uut.version, 1.1)

    def test_variable_int_invalid(self):
        uut = Expression("OKv{f:version}")
        self.assert_(not uut("OKvBAM"))
        self.assert_(not getattr(uut, "version", False))
