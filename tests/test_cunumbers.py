import unittest, cunumbers
_to_cu = cunumbers.to_cu
_to_arab = cunumbers.to_arab

class ToCUTestCase(unittest.TestCase):
    def test_to_cu_digits(self):
        self.assertEqual(_to_cu(1), "а҃")
        self.assertEqual(_to_cu(9), "ѳ҃")
    
    def test_to_cu_tens(self):
        self.assertEqual(_to_cu(10), "і҃")
        self.assertEqual(_to_cu(18), "и҃і")
        self.assertEqual(_to_cu(22), "к҃в")

    def test_to_cu_hundreds(self):
        self.assertEqual(_to_cu(100), "р҃")
        self.assertEqual(_to_cu(207), "с҃з")
        self.assertEqual(_to_cu(333), "тл҃г")

    def test_to_cu_thousand(self):
        self.assertEqual(_to_cu(1000), "҂а҃")
        self.assertEqual(_to_cu(1006), "҂а҃ѕ")
        self.assertEqual(_to_cu(1015), "҂ає҃і")
        self.assertEqual(_to_cu(1444), "҂аум҃д")

    def test_to_cu_big(self):
        self.assertEqual(_to_cu(10001010001), "҂҂҂і҂҂а҂і҃а")
        self.assertEqual(_to_cu(50000000000), "҂҂҂н҃")
        self.assertEqual(_to_cu(60000070000), "҂҂҂ѯ҂ѻ҃")
        
class ToArabTestCase(unittest.TestCase):
    def test_to_arab_digits(self):
        self.assertEqual(1, _to_arab("а҃"))
        self.assertEqual(9, _to_arab("ѳ"))

    def test_to_arab_tens(self):
        self.assertEqual(10, _to_arab("і҃"))
        self.assertEqual(18, _to_arab("и҃і"))
        self.assertEqual(22, _to_arab("к҃в"))

    def test_to_arab_hundreds(self):
        self.assertEqual(100, _to_arab("р҃"))
        self.assertEqual(207, _to_arab("с҃з"))
        self.assertEqual(333, _to_arab("тл҃г"))

    def test_to_arab_thousands(self):
        self.assertEqual(1000, _to_arab("҂а҃"))
        self.assertEqual(1006, _to_arab("҂а҃ѕ"))
        self.assertEqual(1015, _to_arab("҂ає҃і"))
        self.assertEqual(1444, _to_arab("҂аум҃д"))

    def test_to_arab_big(self):
        self.assertEqual(10001010001, _to_arab("҂҂҂і҂҂а҂і҃а"))
        self.assertEqual(50000000000, _to_arab("҂҂҂н҃"))
        self.assertEqual(60000070000, _to_arab("҂҂҂ѯ҂ѻ҃"))

    def test_to_arab_no_tsnd(self):
        self.assertEqual(80500690700, _to_arab("пфхч҃ѱ"))

    def test_to_arab_no_titlo(self):
        self.assertEqual(1, _to_arab("а"))

    def test_to_arab_spaced(self):
        self.assertEqual(1, _to_arab("а҃ "))
    
    def test_to_arab_uppercase(self):
        self.assertEqual(1, _to_arab("А҃"))

    def test_to_arab_mixed(self):
        self.assertEqual(2021, _to_arab(" вКА"))

class ErrorTestCase(unittest.TestCase):
    def test_to_cu_error(self):
        self.assertRaises(TypeError, _to_cu, "String")
        self.assertRaises(TypeError, _to_cu, 9.75)
        self.assertRaises(ValueError, _to_cu, 0)
        self.assertRaises(ValueError, _to_cu, -69)

    def test_to_arab_error(self):
        self.assertRaises(TypeError, _to_arab, 420)
        self.assertRaises(ValueError, _to_arab, "A113")

if __name__ == '__main__':
    unittest.main()