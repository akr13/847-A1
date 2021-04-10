import unittest
from calculator import Calculator

class MyTestCase(unittest.TestCase):
    def test_addition(self):
        instance = Calculator(6, 3)
        self.assertEqual(instance.add(), 9)
    def test_subtraction(self):
        instance = Calculator(6, 3)
        self.assertEqual(instance.sub(), 3)
    def test_division(self):
        instance = Calculator(6, 3)
        self.assertEqual(instance.divide(), 2)
    def test_multiplication(self):
        instance = Calculator(6, 3)
        self.assertEqual(instance.multiply(), 18)


if __name__ == '__main__':
    unittest.main()
