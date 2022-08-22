# -*- coding: UTF-8 -*-
import unittest
from omninumeric.roman import *


class WriteBasicTestCase(unittest.TestCase):
    def testWriteDigits(self):
        self.assertEqual(write(1), "I")
        self.assertEqual(write(2), "II")
        self.assertEqual(write(3), "III")
        self.assertEqual(write(4), "IV")
        self.assertEqual(write(5), "V")
        self.assertEqual(write(6), "VI")
        self.assertEqual(write(7), "VII")
        self.assertEqual(write(8), "VIII")
        self.assertEqual(write(9), "IX")

    def testWriteTens(self):
        self.assertEqual(write(10), "X")
        self.assertEqual(write(20), "XX")
        self.assertEqual(write(30), "XXX")
        self.assertEqual(write(40), "XL")
        self.assertEqual(write(50), "L")
        self.assertEqual(write(60), "LX")
        self.assertEqual(write(70), "LXX")
        self.assertEqual(write(80), "LXXX")
        self.assertEqual(write(90), "XC")

    def testWriteHundreds(self):
        self.assertEqual(write(100), "C")
        self.assertEqual(write(200), "CC")
        self.assertEqual(write(300), "CCC")
        self.assertEqual(write(400), "CD")
        self.assertEqual(write(500), "D")
        self.assertEqual(write(600), "DC")
        self.assertEqual(write(700), "DCC")
        self.assertEqual(write(800), "DCCC")
        self.assertEqual(write(900), "CM")

    def testWriteThousands(self):
        self.assertEqual(write(1000), "M")
        self.assertEqual(write(2000), "MM")
        self.assertEqual(write(3000), "MMM")


class WriteAdvancedTestCase(unittest.TestCase):
    def testWriteTens(self):
        self.assertEqual(write(12), "XII")
        self.assertEqual(write(14), "XIV")
        self.assertEqual(write(18), "XVIII")
        self.assertEqual(write(19), "XIX")
        self.assertEqual(write(33), "XXXIII")
        self.assertEqual(write(45), "XLV")
        self.assertEqual(write(56), "LVI")
        self.assertEqual(write(79), "LXXIX")
        self.assertEqual(write(97), "XCVII")

    def testWriteHundreds(self):
        self.assertEqual(write(164), "CLXIV")
        self.assertEqual(write(222), "CCXXII")
        self.assertEqual(write(477), "CDLXXVII")
        self.assertEqual(write(759), "DCCLIX")
        self.assertEqual(write(999), "CMXCIX")

    def testWriteThousands(self):
        self.assertEqual(write(1919), "MCMXIX")
        self.assertEqual(write(2022), "MMXXII")


class ReadBasicTestCase(unittest.TestCase):
    def testReadDigits(self):
        self.assertEqual(1, read("I"))
        self.assertEqual(2, read("II"))
        self.assertEqual(3, read("III"))
        self.assertEqual(4, read("IV"))
        self.assertEqual(5, read("V"))
        self.assertEqual(6, read("VI"))
        self.assertEqual(7, read("VII"))
        self.assertEqual(8, read("VIII"))
        self.assertEqual(9, read("IX"))

    def testReadTens(self):
        self.assertEqual(10, read("X"))
        self.assertEqual(20, read("XX"))
        self.assertEqual(30, read("XXX"))
        self.assertEqual(40, read("XL"))
        self.assertEqual(50, read("L"))
        self.assertEqual(60, read("LX"))
        self.assertEqual(70, read("LXX"))
        self.assertEqual(80, read("LXXX"))
        self.assertEqual(90, read("XC"))

    def testReadHundreds(self):
        self.assertEqual(100, read("C"))
        self.assertEqual(200, read("CC"))
        self.assertEqual(300, read("CCC"))
        self.assertEqual(400, read("CD"))
        self.assertEqual(500, read("D"))
        self.assertEqual(600, read("DC"))
        self.assertEqual(700, read("DCC"))
        self.assertEqual(800, read("DCCC"))
        self.assertEqual(900, read("CM"))

    def testReadThousands(self):
        self.assertEqual(1000, read("M"))
        self.assertEqual(2000, read("MM"))
        self.assertEqual(3000, read("MMM"))


class ReadAdvancedTestCase(unittest.TestCase):
    def testReadTens(self):
        self.assertEqual(12, read("XII"))
        self.assertEqual(14, read("XIV"))
        self.assertEqual(18, read("XVIII"))
        self.assertEqual(19, read("XIX"))
        self.assertEqual(33, read("XXXIII"))
        self.assertEqual(45, read("XLV"))
        self.assertEqual(56, read("LVI"))
        self.assertEqual(79, read("LXXIX"))
        self.assertEqual(97, read("XCVII"))

    def testReadHundreds(self):
        self.assertEqual(164, read("CLXIV"))
        self.assertEqual(222, read("CCXXII"))
        self.assertEqual(477, read("CDLXXVII"))
        self.assertEqual(759, read("DCCLIX"))
        self.assertEqual(999, read("CMXCIX"))

    def testReadThousands(self):
        self.assertEqual(1919, read("MCMXIX"))
        self.assertEqual(2022, read("MMXXII"))


class ReadExtendedTestCase(unittest.TestCase):
    def testReadExtended(self):
        self.assertEqual(1900019, read("M̅C̅M̅XIX"))
        self.assertEqual(1001022, read("M̅MXXII"))


if __name__ == "__main__":
    unittest.main()
