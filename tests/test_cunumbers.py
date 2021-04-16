import unittest, cunumbers
arab_to_cu = cunumbers.arab_to_cu
cu_to_arab = cunumbers.cu_to_arab

class arab_to_cuTestCase(unittest.TestCase):
    def test_arab_to_cu_digits(self):
        self.assertEqual(arab_to_cu(1), "а҃")
        self.assertEqual(arab_to_cu(9), "ѳ҃")
    
    def test_arab_to_cu_tens(self):
        self.assertEqual(arab_to_cu(10), "і҃")
        self.assertEqual(arab_to_cu(18), "и҃і")
        self.assertEqual(arab_to_cu(22), "к҃в")

    def test_arab_to_cu_hundreds(self):
        self.assertEqual(arab_to_cu(100), "р҃")
        self.assertEqual(arab_to_cu(207), "с҃з")
        self.assertEqual(arab_to_cu(333), "тл҃г")

    def test_arab_to_cu_thousand(self):
        self.assertEqual(arab_to_cu(1000), "҂а҃")
        self.assertEqual(arab_to_cu(1006), "҂аѕ҃")
        self.assertEqual(arab_to_cu(1015), "҂ає҃і")
        self.assertEqual(arab_to_cu(1444), "҂аум҃д")

    def test_arab_to_cu_big(self):
        self.assertEqual(arab_to_cu(10001010001), "҂҂҂і҂҂а҂іа҃")
        self.assertEqual(arab_to_cu(50000000000), "҂҂҂н҃")
        self.assertEqual(arab_to_cu(60000070000), "҂҂҂ѯ҂ѻ҃")
        
class cu_to_arabTestCase(unittest.TestCase):
    def test_cu_to_arab_digits(self):
        self.assertEqual(1, cu_to_arab("а҃"))
        self.assertEqual(9, cu_to_arab("ѳ"))

    def test_cu_to_arab_tens(self):
        self.assertEqual(10, cu_to_arab("і҃"))
        self.assertEqual(18, cu_to_arab("и҃і"))
        self.assertEqual(22, cu_to_arab("к҃в"))

    def test_cu_to_arab_hundreds(self):
        self.assertEqual(100, cu_to_arab("р҃"))
        self.assertEqual(207, cu_to_arab("с҃з"))
        self.assertEqual(333, cu_to_arab("тл҃г"))

    def test_cu_to_arab_thousands(self):
        self.assertEqual(1000, cu_to_arab("҂а҃"))
        self.assertEqual(1006, cu_to_arab("҂аѕ҃"))
        self.assertEqual(1015, cu_to_arab("҂ає҃і"))
        self.assertEqual(1444, cu_to_arab("҂аум҃д"))

    def test_cu_to_arab_big(self):
        self.assertEqual(10001010001, cu_to_arab("҂҂҂і҂҂а҂іа҃"))
        self.assertEqual(50000000000, cu_to_arab("҂҂҂н҃"))
        self.assertEqual(60000070000, cu_to_arab("҂҂҂ѯ҂ѻ҃"))

    def test_cu_to_arab_no_tsnd(self):
        self.assertEqual(80500690700, cu_to_arab("пфхчѱ҃"))

    def test_cu_to_arab_no_titlo(self):
        self.assertEqual(1, cu_to_arab("а"))

    def test_cu_to_arab_spaced(self):
        self.assertEqual(1, cu_to_arab("а҃ "))
    
    def test_cu_to_arab_uppercase(self):
        self.assertEqual(1, cu_to_arab("А҃"))

    def test_cu_to_arab_mixed(self):
        self.assertEqual(2021, cu_to_arab(" вКА"))

class ErrorTestCase(unittest.TestCase):
    def test_arab_to_cu_error(self):
        self.assertRaises(TypeError, arab_to_cu, "String")
        self.assertRaises(TypeError, arab_to_cu, 9.75)
        self.assertRaises(ValueError, arab_to_cu, 0)
        self.assertRaises(ValueError, arab_to_cu, -69)

    def test_cu_to_arab_error(self):
        self.assertRaises(TypeError, cu_to_arab, 420)
        self.assertRaises(ValueError, cu_to_arab, "A113")

if __name__ == '__main__':
    unittest.main()