# -*- coding: UTF-8 -*-
import unittest
from cunumbers.cunumbers import *


class ToCUPlainTestCase(unittest.TestCase):
    def testToCUDigits(self):
        self.assertEqual(toCU(1), "а҃")
        self.assertEqual(toCU(9), "ѳ҃")

    def testToCUTens(self):
        self.assertEqual(toCU(10), "і҃")
        self.assertEqual(toCU(18), "и҃і")
        self.assertEqual(toCU(22), "к҃в")

    def testToCUHundreds(self):
        self.assertEqual(toCU(100), "р҃")
        self.assertEqual(toCU(207), "с҃з")
        self.assertEqual(toCU(333), "тл҃г")

    def testToCUThousand(self):
        self.assertEqual(toCU(1000), "҂а҃")
        self.assertEqual(toCU(1006, CU_PLAIN), "҂а҃ѕ")
        self.assertEqual(toCU(1010, CU_PLAIN), "҂а҃і")
        self.assertEqual(toCU(1015), "҂ає҃і")
        self.assertEqual(toCU(1444), "҂аум҃д")
        self.assertEqual(toCU(11000, CU_PLAIN), "҂і҂а҃")

    def testToCUBig(self):
        self.assertEqual(toCU(10001010001, CU_PLAIN), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(toCU(50000000000, CU_PLAIN), "҂҂҂н҃")
        self.assertEqual(toCU(60000070000, CU_PLAIN), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(toCU(111111111, CU_PLAIN), "҂҂р҂҂і҂҂а҂р҂і҂ара҃і")


class ToCUDelimTestCase(unittest.TestCase):
    def testToCUDelimThousand(self):
        self.assertEqual(toCU(1010), "҂а.і҃")
        self.assertEqual(toCU(11000), "҂а҃і")

    def testToCUDelimBig(self):
        self.assertEqual(toCU(10001010001), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(toCU(50000000000), "҂҂҂н҃")
        self.assertEqual(toCU(60000070000), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(toCU(111111111), "҂҂раі҂раіра҃і")


class ToCUFlagsTestCase(unittest.TestCase):
    def testToCUNotitlo(self):
        self.assertEqual(toCU(1, CU_NOTITLO), "а")
        self.assertEqual(toCU(11000, CU_PLAIN + CU_NOTITLO), "҂і҂а")

    def testToCUEnddot(self):
        self.assertEqual(toCU(1, CU_ENDDOT), "а҃.")

    def testToCUWrapdot(self):
        self.assertEqual(toCU(1, CU_WRAPDOT), ".а҃.")

    def testToCUDelimdot(self):
        self.assertEqual(toCU(1001, CU_DELIMDOT), "҂а.а҃")
        self.assertEqual(toCU(1010, CU_DELIMDOT), "҂а.і҃")
        self.assertEqual(toCU(11000, CU_DELIMDOT), "҂а҃і")
        self.assertEqual(toCU(111111111, CU_DELIMDOT), "҂҂раі.҂раі.ра҃і")

    def testToCUAlldot(self):
        self.assertEqual(toCU(1001, CU_ALLDOT), ".҂а.а҃.")

    def testToCUDotscustom(self):
        self.assertEqual(toCU(1001, CU_ENDDOT + CU_DELIMDOT), "҂а.а҃.")


class ToArabDelimTestCase(unittest.TestCase):
    def testToArabDigits(self):
        self.assertEqual(1, toArab("а҃"))
        self.assertEqual(9, toArab("ѳ"))

    def testToArabTens(self):
        self.assertEqual(10, toArab("і҃"))
        self.assertEqual(18, toArab("и҃і"))
        self.assertEqual(22, toArab("к҃в"))

    def testToArabHundreds(self):
        self.assertEqual(100, toArab("р҃"))
        self.assertEqual(207, toArab("с҃з"))
        self.assertEqual(333, toArab("тл҃г"))

    def testToArabThousands(self):
        self.assertEqual(1000, toArab("҂а҃"))
        self.assertEqual(1006, toArab("҂а҃ѕ"))
        self.assertEqual(1015, toArab("҂ає҃і"))
        self.assertEqual(1444, toArab("҂аум҃д"))

    def testToArabBig(self):
        self.assertEqual(10001010001, toArab("҂҂҂і҂҂а҂і҃а"))
        self.assertEqual(50000000000, toArab("҂҂҂н҃"))
        self.assertEqual(60000070000, toArab("҂҂҂ѯ҂ѻ҃"))

    def testToArabNoTsnd(self):
        self.assertEqual(80500690700, toArab("пфхч҃ѱ"))

    def testToArabNotitlo(self):
        self.assertEqual(1, toArab("а"))

    def testToArabSpaced(self):
        self.assertEqual(1, toArab("а҃ "))

    def testToArabUppercase(self):
        self.assertEqual(1, toArab("А҃"))

    def testToArabMixed(self):
        self.assertEqual(2021, toArab(" вКА"))


class ToArabPlainTestCase(unittest.TestCase):
    def testToArabPlainBig(self):
        self.assertEqual(11000, toArab("҂і҂а"))
        self.assertEqual(111111111, toArab("҂҂р҂҂і҂҂а҂р҂і҂ара҃і"))


class ErrorTestCase(unittest.TestCase):
    def testToCUError(self):
        self.assertEqual(None, toCU("String"))
        self.assertEqual(None, toCU(9.75))
        self.assertEqual(None, toCU(0))
        self.assertEqual(None, toCU(-69))

    def testToArabError(self):
        self.assertEqual(None, toArab(420))
        self.assertEqual(None, toArab(""))
        self.assertEqual(None, toArab("A113"))


if __name__ == "__main__":
    unittest.main()
