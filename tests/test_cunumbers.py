import unittest
from cunumbers import *

class ToCUPlainTestCase(unittest.TestCase):
    def test_to_cu_digits(self):
        self.assertEqual(to_cu(1), "а҃")
        self.assertEqual(to_cu(9), "ѳ҃")
    
    def test_to_cu_tens(self):
        self.assertEqual(to_cu(10), "і҃")
        self.assertEqual(to_cu(18), "и҃і")
        self.assertEqual(to_cu(22), "к҃в")

    def test_to_cu_hundreds(self):
        self.assertEqual(to_cu(100), "р҃")
        self.assertEqual(to_cu(207), "с҃з")
        self.assertEqual(to_cu(333), "тл҃г")

    def test_to_cu_thousand(self):
        self.assertEqual(to_cu(1000), "҂а҃")
        self.assertEqual(to_cu(1006), "҂а҃ѕ")
        self.assertEqual(to_cu(1015), "҂ає҃і")
        self.assertEqual(to_cu(1444), "҂аум҃д")
        self.assertEqual(to_cu(11000, CU_PLAIN), "҂і҂а҃")

    def test_to_cu_big(self):
        self.assertEqual(to_cu(10001010001, CU_PLAIN), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(to_cu(50000000000, CU_PLAIN), "҂҂҂н҃")
        self.assertEqual(to_cu(60000070000, CU_PLAIN), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(to_cu(111111111, CU_PLAIN), "҂҂р҂҂і҂҂а҂р҂і҂ара҃і")

class ToCUDelimTestCase(unittest.TestCase):

    def test_to_cu_delim_digits(self):
        self.assertEqual(to_cu(1, CU_DELIM), "а҃")
    
    def test_to_cu_delim_tens(self):
        self.assertEqual(to_cu(18, CU_DELIM), "и҃і")

    def test_to_cu_delim_hundreds(self):
        self.assertEqual(to_cu(833, CU_DELIM), "ѿл҃г")

    def test_to_cu__delim_thousand(self):
        self.assertEqual(to_cu(1444, CU_DELIM), "҂аум҃д")
        self.assertEqual(to_cu(11000), "҂а҃і")

    def test_to_cu_delim_big(self):
        self.assertEqual(to_cu(10001010001), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(to_cu(50000000000), "҂҂҂н҃")
        self.assertEqual(to_cu(60000070000), "҂҂҂ѯ҂ѻ҃")
        self.assertEqual(to_cu(111111111), "҂҂раі҂раіра҃і")

class ToCUFlagsTestCase(unittest.TestCase):
    def test_to_cu_notitlo(self):
        self.assertEqual(to_cu(1, CU_NOTITLO), "а")
        self.assertEqual(to_cu(11000, CU_PLAIN + CU_NOTITLO), "҂і҂а")

    def test_to_cu_enddot(self):
        self.assertEqual(to_cu(1, CU_ENDDOT), "а҃.")

    def test_to_cu_twodots(self):
        self.assertEqual(to_cu(1, CU_TWODOTS), ".а҃.")

    def test_to_cu_deldot(self):
        self.assertEqual(to_cu(1001, CU_DELIM + CU_DELDOT), "҂а.а҃")
        
class ToArabDelimTestCase(unittest.TestCase):
    def test_to_arab_digits(self):
        self.assertEqual(1, to_arab("а҃"))
        self.assertEqual(9, to_arab("ѳ"))

    def test_to_arab_tens(self):
        self.assertEqual(10, to_arab("і҃"))
        self.assertEqual(18, to_arab("и҃і"))
        self.assertEqual(22, to_arab("к҃в"))

    def test_to_arab_hundreds(self):
        self.assertEqual(100, to_arab("р҃"))
        self.assertEqual(207, to_arab("с҃з"))
        self.assertEqual(333, to_arab("тл҃г"))

    def test_to_arab_thousands(self):
        self.assertEqual(1000, to_arab("҂а҃"))
        self.assertEqual(1006, to_arab("҂а҃ѕ"))
        self.assertEqual(1015, to_arab("҂ає҃і"))
        self.assertEqual(1444, to_arab("҂аум҃д"))

    def test_to_arab_big(self):
        self.assertEqual(10001010001, to_arab("҂҂҂і҂҂а҂і҃а"))
        self.assertEqual(50000000000, to_arab("҂҂҂н҃"))
        self.assertEqual(60000070000, to_arab("҂҂҂ѯ҂ѻ҃"))

    def test_to_arab_no_tsnd(self):
        self.assertEqual(80500690700, to_arab("пфхч҃ѱ"))

    def test_to_arab_notitlo(self):
        self.assertEqual(1, to_arab("а"))

    def test_to_arab_spaced(self):
        self.assertEqual(1, to_arab("а҃ "))
    
    def test_to_arab_uppercase(self):
        self.assertEqual(1, to_arab("А҃"))

    def test_to_arab_mixed(self):
        self.assertEqual(2021, to_arab(" вКА"))

class ToArabPlainTestCase(unittest.TestCase):
    def test_to_arab_plain_big(self):
        self.assertEqual(11000, to_arab("҂і҂а"))
        self.assertEqual(111111111, to_arab("҂҂р҂҂і҂҂а҂р҂і҂ара҃і"))

class ErrorTestCase(unittest.TestCase):
    def test_to_cu_error(self):
        self.assertRaises(TypeError, to_cu, "String")
        self.assertRaises(TypeError, to_cu, 9.75)
        self.assertRaises(ValueError, to_cu, 0)
        self.assertRaises(ValueError, to_cu, -69)

    def test_to_arab_error(self):
        self.assertRaises(TypeError, to_arab, 420)
        self.assertRaises(ValueError, to_arab, "")
        self.assertRaises(ValueError, to_arab, "A113")

if __name__ == '__main__':
    unittest.main()