# -*- coding: UTF-8 -*-
import unittest
from cunumbers.cunumbers import *


class ToCUPlainTestCase(unittest.TestCase):
    def testToCUDigits(self):
        self.assertEqual(to_cu(1), "а҃")
        self.assertEqual(to_cu(9), "ѳ҃")

    def testToCUTens(self):
        self.assertEqual(to_cu(10), "і҃")
        self.assertEqual(to_cu(18), "и҃і")
        self.assertEqual(to_cu(22), "к҃в")

    def testToCUHundreds(self):
        self.assertEqual(to_cu(100), "р҃")
        self.assertEqual(to_cu(207), "с҃з")
        self.assertEqual(to_cu(333), "тл҃г")

    def testToCUThousand(self):
        self.assertEqual(to_cu(1000), "҂а҃")
        self.assertEqual(to_cu(1006, CU_PLAIN), "҂а҃ѕ")
        self.assertEqual(to_cu(1010, CU_PLAIN), "҂а҃і")
        self.assertEqual(to_cu(1015), "҂ає҃і")
        self.assertEqual(to_cu(1444), "҂аум҃д")
        self.assertEqual(to_cu(11000, CU_PLAIN), "҂і҂а҃")

    def testToCUBig(self):
        self.assertEqual(to_cu(10001010001, CU_PLAIN), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(to_cu(50000000000, CU_PLAIN), "҂҂҂н҃")
        self.assertEqual(to_cu(60000070000, CU_PLAIN), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(to_cu(111111111, CU_PLAIN), "҂҂р҂҂і҂҂а҂р҂і҂ара҃і")


class ToCUDelimTestCase(unittest.TestCase):
    def testToCUDelimThousand(self):
        self.assertEqual(to_cu(1010), "҂а.і҃")
        self.assertEqual(to_cu(11000), "҂а҃і")

    def testToCUDelimBig(self):
        self.assertEqual(to_cu(10001010001), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(to_cu(50000000000), "҂҂҂н҃")
        self.assertEqual(to_cu(60000070000), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(to_cu(111111111), "҂҂раі҂раіра҃і")


class ToCUFlagsTestCase(unittest.TestCase):
    def testToCUNotitlo(self):
        self.assertEqual(to_cu(1, CU_NOTITLO), "а")
        self.assertEqual(to_cu(11000, CU_PLAIN + CU_NOTITLO), "҂і҂а")

    def testToCUEnddot(self):
        self.assertEqual(to_cu(1, CU_ENDDOT), "а҃.")

    def testToCUWrapdot(self):
        self.assertEqual(to_cu(1, CU_WRAPDOT), ".а҃.")

    def testToCUDelimdot(self):
        self.assertEqual(to_cu(1001, CU_DELIMDOT), "҂а.а҃")
        self.assertEqual(to_cu(1010, CU_DELIMDOT), "҂а.і҃")
        self.assertEqual(to_cu(11000, CU_DELIMDOT), "҂а҃і")
        self.assertEqual(to_cu(111111111, CU_DELIMDOT), "҂҂раі.҂раі.ра҃і")

    def testToCUAlldot(self):
        self.assertEqual(to_cu(1001, CU_ALLDOT), ".҂а.а҃.")

    def testToCUDotscustom(self):
        self.assertEqual(to_cu(1001, CU_ENDDOT + CU_DELIMDOT), "҂а.а҃.")


class ToArabDelimTestCase(unittest.TestCase):
    def testToArabDigits(self):
        self.assertEqual(1, to_arab("а҃"))
        self.assertEqual(9, to_arab("ѳ"))

    def testToArabTens(self):
        self.assertEqual(10, to_arab("і҃"))
        self.assertEqual(18, to_arab("и҃і"))
        self.assertEqual(22, to_arab("к҃в"))

    def testToArabHundreds(self):
        self.assertEqual(100, to_arab("р҃"))
        self.assertEqual(207, to_arab("с҃з"))
        self.assertEqual(333, to_arab("тл҃г"))

    def testToArabThousands(self):
        self.assertEqual(1000, to_arab("҂а҃"))
        self.assertEqual(1006, to_arab("҂а҃ѕ"))
        self.assertEqual(1015, to_arab("҂ає҃і"))
        self.assertEqual(1444, to_arab("҂аум҃д"))

    def testToArabBig(self):
        self.assertEqual(10001010001, to_arab("҂҂҂і҂҂а҂і҃а"))
        self.assertEqual(50000000000, to_arab("҂҂҂н҃"))
        self.assertEqual(60000070000, to_arab("҂҂҂ѯ҂ѻ҃"))

    def testToArabNoTsnd(self):
        self.assertEqual(80500690700, to_arab("пфхч҃ѱ"))

    def testToArabNotitlo(self):
        self.assertEqual(1, to_arab("а"))

    def testToArabSpaced(self):
        self.assertEqual(1, to_arab("а҃ "))

    def testToArabUppercase(self):
        self.assertEqual(1, to_arab("А҃"))

    def testToArabMixed(self):
        self.assertEqual(2021, to_arab(" вКА"))


class ToArabPlainTestCase(unittest.TestCase):
    def testToArabPlainBig(self):
        self.assertEqual(11000, to_arab("҂і҂а"))
        self.assertEqual(111111111, to_arab("҂҂р҂҂і҂҂а҂р҂і҂ара҃і"))


class ErrorTestCase(unittest.TestCase):
    def testToCUError(self):
        self.assertEqual(None, to_cu("String"))
        self.assertEqual(None, to_cu(9.75))
        self.assertEqual(None, to_cu(0))
        self.assertEqual(None, to_cu(-69))

    def testToArabError(self):
        self.assertEqual(None, to_arab(420))
        self.assertEqual(None, to_arab(""))
        self.assertEqual(None, to_arab("A113"))


if __name__ == "__main__":
    unittest.main()
