# -*- coding: UTF-8 -*-
import unittest
from omninumeric.cyrillic import *


class WritePlainTestCase(unittest.TestCase):
    def testWriteDigits(self):
        self.assertEqual(write(1), "а҃")
        self.assertEqual(write(9), "ѳ҃")

    def testWriteTens(self):
        self.assertEqual(write(10), "і҃")
        self.assertEqual(write(18), "и҃і")
        self.assertEqual(write(22), "к҃в")

    def testWriteHundreds(self):
        self.assertEqual(write(100), "р҃")
        self.assertEqual(write(207), "с҃з")
        self.assertEqual(write(333), "тл҃г")

    def testWriteThousand(self):
        self.assertEqual(write(1000), "҂а҃")
        self.assertEqual(write(1006), "҂а҃ѕ")
        self.assertEqual(write(1010), "҂а҃і")
        self.assertEqual(write(1015), "҂ає҃і")
        self.assertEqual(write(1444), "҂аум҃д")
        self.assertEqual(write(11000), "҂і҂а҃")

    def testWriteBig(self):
        self.assertEqual(write(10001010001), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(write(50000000000), "҂҂҂н҃")
        self.assertEqual(write(60000070000), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(write(111111111), "҂҂р҂҂і҂҂а҂р҂і҂ара҃і")


class WriteDelimTestCase(unittest.TestCase):
    def testWriteDelimAmbiguity(self):
        self.assertEqual(write(1010, DELIM), "҂а.і҃")
        self.assertEqual(write(11000, DELIM), "҂а҃і")
        self.assertEqual(write(10010, DELIM), "҂і҃і")
        self.assertEqual(write(110010, DELIM), "҂рі҃і")
        self.assertEqual(write(100010, DELIM), "҂р.і҃")
        self.assertEqual(write(110000, DELIM), "҂р҃і")
        self.assertEqual(write(100011, DELIM), "҂р.а҃і")
        self.assertEqual(write(111000, DELIM), "҂ра҃і")

    def testWriteDelimBig(self):
        self.assertEqual(write(10001010001, DELIM), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(write(50000000000, DELIM), "҂҂҂н҃")
        self.assertEqual(write(60000070000, DELIM), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(write(111111111, DELIM), "҂҂раі҂раіра҃і")


class WriteFlagsTestCase(unittest.TestCase):
    def testWriteNotitlo(self):
        self.assertEqual(write(1, NOTITLO), "а")
        self.assertEqual(write(11000, NOTITLO), "҂і҂а")

    def testWriteEnddot(self):
        self.assertEqual(write(1, ENDDOT), "а҃.")

    def testWriteWrapdot(self):
        self.assertEqual(write(1, WRAPDOT), ".а҃.")

    def testWriteDelimdot(self):
        self.assertEqual(write(1001, DELIMDOT), "҂а.а҃")
        self.assertEqual(write(1010, DELIMDOT), "҂а.і҃")
        self.assertEqual(write(11000, DELIMDOT), "҂а҃і")
        self.assertEqual(write(111111111, DELIMDOT), "҂҂раі.҂раі.ра҃і")

    def testWriteAlldot(self):
        self.assertEqual(write(1001, ALLDOT), ".҂а.а҃.")

    def testWriteDotscustom(self):
        self.assertEqual(write(1001, ENDDOT + DELIMDOT), "҂а.а҃.")


class ReadDelimTestCase(unittest.TestCase):
    def testReadDigits(self):
        self.assertEqual(1, read("а҃"))
        self.assertEqual(9, read("ѳ"))

    def testReadTens(self):
        self.assertEqual(10, read("і҃"))
        self.assertEqual(18, read("и҃і"))
        self.assertEqual(22, read("к҃в"))

    def testReadHundreds(self):
        self.assertEqual(100, read("р҃"))
        self.assertEqual(207, read("с҃з"))
        self.assertEqual(333, read("тл҃г"))

    def testReadThousands(self):
        self.assertEqual(1000, read("҂а҃"))
        self.assertEqual(1006, read("҂а҃ѕ"))
        self.assertEqual(1015, read("҂ає҃і"))
        self.assertEqual(1444, read("҂аум҃д"))

    def testReadBig(self):
        self.assertEqual(10001010001, read("҂҂҂і҂҂а҂і҃а"))
        self.assertEqual(50000000000, read("҂҂҂н҃"))
        self.assertEqual(60000070000, read("҂҂҂ѯ҂ѻ҃"))

    def testReadNoTsnd(self):
        self.assertEqual(80500690700, read("пфхч҃ѱ"))

    def testReadNotitlo(self):
        self.assertEqual(1, read("а"))

    def testReadSpaced(self):
        self.assertEqual(1, read("а҃ "))

    def testReadUppercase(self):
        self.assertEqual(1, read("А҃"))

    def testReadMixed(self):
        self.assertEqual(2021, read(" вКА"))


class ReadPlainTestCase(unittest.TestCase):
    def testReadPlainBig(self):
        self.assertEqual(11000, read("҂і҂а"))
        self.assertEqual(111111111, read("҂҂р҂҂і҂҂а҂р҂і҂ара҃і"))


class ErrorTestCase(unittest.TestCase):
    def testWriteError(self):
        self.assertRaises(TypeError, write, "String")
        self.assertRaises(TypeError, write, 9.75)
        self.assertRaises(ValueError, write, 0)
        self.assertRaises(ValueError, write, -69)

    def testReadError(self):
        self.assertRaises(TypeError, read, 420)
        self.assertRaises(ValueError, read, "")
        self.assertRaises(ValueError, read, "A113")


if __name__ == "__main__":
    unittest.main()
