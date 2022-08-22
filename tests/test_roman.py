# -*- coding: UTF-8 -*-
import unittest
from omninumeric.roman import *


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


if __name__ == "__main__":
    unittest.main()
