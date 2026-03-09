

from django.test import TestCase
from .models import Calculations
# Create your tests here.

def test_add():
    
    TestCase.assertEqual(Calculations.add(2, 3), 5)
    TestCase.assertEqual(Calculations.add(-1, 1), 0)
    TestCase.assertFalse(Calculations.add(-2, -3), 5)
    TestCase.assertFalse(Calculations.add(2,2), 5)
    TestCase.assertRaises(TypeError, Calculations.add, 2, "3")
    
    

def test_divide():
   
    TestCase.assertEqual(Calculations.divide(10, 2), 5)
    TestCase.assertEqual(Calculations.divide(-4, 2), -2)
    TestCase.assertEqual(Calculations.divide(0, 1), 0)
    TestCase.assertRaises(ZeroDivisionError, Calculations.divide, 5, 0)

def test_subtract():

    TestCase.assertEqual(Calculations.subtract(5, 3), 2)
    TestCase.assertEqual(Calculations.subtract(-1, 1), -2)
    TestCase.assertFalse(Calculations.subtract(2,2), 1)
    TestCase.assertFalse(Calculations.subtract(5, 3), 3)

def test_multiply():
    
    TestCase.assertEqual(Calculations.multiply(4, 5), 20)
    TestCase.assertEqual(Calculations.multiply(-2, 3), -6)
    TestCase.assertEqual(Calculations.multiply(0, 10), 0)

TestCase.run()
