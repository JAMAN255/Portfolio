
"""
Comprehensive tests for calculator application.
Tests calculations, index calculations, and views.
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import Calculations


class CalculationsBasicTest(TestCase):
    """Test basic arithmetic calculations"""

    def test_add_positive_numbers(self):
        """Test addition of positive numbers"""
        result = Calculations.add(5, 3)
        self.assertEqual(result, 8.0)

    def test_add_negative_numbers(self):
        """Test addition with negative numbers"""
        result = Calculations.add(-5, -3)
        self.assertEqual(result, -8.0)

    def test_add_mixed_signs(self):
        """Test addition with mixed signs"""
        result = Calculations.add(5, -3)
        self.assertEqual(result, 2.0)

    def test_add_float_numbers(self):
        """Test addition of float numbers"""
        result = Calculations.add(5.5, 3.2)
        self.assertAlmostEqual(result, 8.7, places=5)

    def test_add_strings_to_numbers(self):
        """Test addition converts strings to numbers"""
        result = Calculations.add('5', '3')
        self.assertEqual(result, 8.0)

    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers"""
        result = Calculations.subtract(10, 3)
        self.assertEqual(result, 7.0)

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative"""
        result = Calculations.subtract(3, 10)
        self.assertEqual(result, -7.0)

    def test_subtract_float_numbers(self):
        """Test subtraction of float numbers"""
        result = Calculations.subtract(10.5, 3.2)
        self.assertAlmostEqual(result, 7.3, places=5)

    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers"""
        result = Calculations.multiply(5, 3)
        self.assertEqual(result, 15.0)

    def test_multiply_by_zero(self):
        """Test multiplication by zero"""
        result = Calculations.multiply(5, 0)
        self.assertEqual(result, 0.0)

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers"""
        result = Calculations.multiply(-5, -3)
        self.assertEqual(result, 15.0)

    def test_multiply_float_numbers(self):
        """Test multiplication of float numbers"""
        result = Calculations.multiply(2.5, 4.0)
        self.assertEqual(result, 10.0)

    def test_divide_positive_numbers(self):
        """Test division of positive numbers"""
        result = Calculations.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_divide_float_result(self):
        """Test division resulting in float"""
        result = Calculations.divide(10, 3)
        self.assertAlmostEqual(result, 3.333333, places=5)

    def test_divide_negative_numbers(self):
        """Test division with negative numbers"""
        result = Calculations.divide(-10, 2)
        self.assertEqual(result, -5.0)


class CalculatorViewTest(TestCase):
    """Test calculator view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('calculator')

    def test_calculator_get_status_code(self):
        """Test calculator view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_calculator_view_template(self):
        """Test calculator view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'calculator/calculator.html')

    def test_calculator_addition(self):
        """Test calculator view performs addition"""
        data = {
            'x': '10',
            'y': '5',
            'operator': '+'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)
        self.assertEqual(response.context['result'], 15.0)

    def test_calculator_subtraction(self):
        """Test calculator view performs subtraction"""
        data = {
            'x': '10',
            'y': '3',
            'operator': '-'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.context['result'], 7.0)

    def test_calculator_multiplication(self):
        """Test calculator view performs multiplication"""
        data = {
            'x': '5',
            'y': '4',
            'operator': '*'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.context['result'], 20.0)

    def test_calculator_division(self):
        """Test calculator view performs division"""
        data = {
            'x': '20',
            'y': '4',
            'operator': '/'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.context['result'], 5.0)

    def test_calculator_division_by_zero(self):
        """Test calculator view handles division by zero"""
        data = {
            'x': '10',
            'y': '0',
            'operator': '/'
        }
        response = self.client.post(self.url, data)
        self.assertIn('error_msg', response.context)
        self.assertIn('Cannot divide by zero', response.context['error_msg'])

    def test_calculator_invalid_operator(self):
        """Test calculator view handles invalid operator"""
        data = {
            'x': '10',
            'y': '5',
            'operator': '%'
        }
        response = self.client.post(self.url, data)
        self.assertIn('error_msg', response.context)
        self.assertIn('Invalid operation', response.context['error_msg'])

    def test_calculator_invalid_input(self):
        """Test calculator view handles invalid input"""
        data = {
            'x': 'abc',
            'y': '5',
            'operator': '+'
        }
        response = self.client.post(self.url, data)
        self.assertIn('error_msg', response.context)
        self.assertIn('Please enter valid numbers', response.context['error_msg'])

    def test_calculator_float_input(self):
        """Test calculator view handles float input"""
        data = {
            'x': '10.5',
            'y': '2.5',
            'operator': '+'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.context['result'], 13.0)


class CalculatorIntegrationTest(TestCase):
    """Integration tests for calculator views"""

    def setUp(self):
        self.client = Client()

    def test_calculator_workflow(self):
        """Test complete calculator workflow"""
        # Test basic calculator operations
        calc_url = reverse('calculator')
        
        # Addition
        response = self.client.post(calc_url, {
            'x': '5', 'y': '3', 'operator': '+'
        })
        self.assertEqual(response.context['result'], 8.0)
        
        # Subtraction
        response = self.client.post(calc_url, {
            'x': '10', 'y': '7', 'operator': '-'
        })
        self.assertEqual(response.context['result'], 3.0)
        
        # Multiplication
        response = self.client.post(calc_url, {
            'x': '4', 'y': '5', 'operator': '*'
        })
        self.assertEqual(response.context['result'], 20.0)
        
        # Division
        response = self.client.post(calc_url, {
            'x': '20', 'y': '5', 'operator': '/'
        })
        self.assertEqual(response.context['result'], 4.0)
