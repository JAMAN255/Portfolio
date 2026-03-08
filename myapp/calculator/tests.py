from django.test import TestCase

# Create your tests here.

def test_add():
    from .models import add
    TestCase.assertEqual(add(2, 3), 5)
    TestCase.assertEqual(add(-1, 1), 0)
    TestCase.assertFalse(add(-2, -3), 5)
    TestCase.assertFalse(add(2,2), 5)
    TestCase.assertRaises(TypeError, add, 2, "3")
    
    

def test_divide():
    from .models import divide
    TestCase.assertEqual(divide(10, 2), 5)
    TestCase.assertEqual(divide(-4, 2), -2)
    TestCase.assertEqual(divide(0, 1), 0)
    TestCase.assertRaises(ZeroDivisionError, divide, 5, 0)

def test_subtract():
    from .models import subtract
    TestCase.assertEqual(subtract(5, 3), 2)
    TestCase.assertEqual(subtract(-1, 1), -2)
    TestCase.assertFalse(subtract(2,2), 1)
    TestCase.assertFalse(subtract(5, 3), 3)

def test_multiply():
    from .models import multiply
    TestCase.assertEqual(multiply(4, 5), 20)
    TestCase.assertEqual(multiply(-2, 3), -6)
    TestCase.assertEqual(multiply(0, 10), 0)

TestCase.run()
