
"""
Comprehensive tests for calculator application.
Tests calculations, index calculations, and views.
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import Calculations, IndexCalculations


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


class CalculationsMeanTest(TestCase):
    """Test mean calculation"""

    def test_mean_simple_list(self):
        """Test mean of simple list"""
        result = Calculations.mean([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)

    def test_mean_single_element(self):
        """Test mean of single element"""
        result = Calculations.mean([5])
        self.assertEqual(result, 5.0)

    def test_mean_negative_numbers(self):
        """Test mean with negative numbers"""
        result = Calculations.mean([-1, -2, -3])
        self.assertEqual(result, -2.0)

    def test_mean_float_numbers(self):
        """Test mean of float numbers"""
        result = Calculations.mean([1.5, 2.5, 3.5])
        self.assertEqual(result, 2.5)

    def test_mean_large_list(self):
        """Test mean of large list"""
        data = list(range(1, 101))
        result = Calculations.mean(data)
        self.assertEqual(result, 50.5)


class CalculationsMedianTest(TestCase):
    """Test median calculation"""

    def test_median_odd_length_list(self):
        """Test median of odd length list"""
        result = Calculations.median([1, 2, 3, 4, 5])
        self.assertEqual(result, 3)

    def test_median_even_length_list(self):
        """Test median of even length list"""
        result = Calculations.median([1, 2, 3, 4])
        self.assertEqual(result, 2.5)

    def test_median_single_element(self):
        """Test median of single element"""
        result = Calculations.median([5])
        self.assertEqual(result, 5)

    def test_median_unsorted_list(self):
        """Test median handles unsorted list"""
        result = Calculations.median([5, 1, 3, 2, 4])
        self.assertEqual(result, 3)

    def test_median_negative_numbers(self):
        """Test median with negative numbers"""
        result = Calculations.median([-5, -3, -1])
        self.assertEqual(result, -3)


class CalculationsModeTest(TestCase):
    """Test mode calculation"""

    def test_mode_single_mode(self):
        """Test mode with single most frequent value"""
        result = Calculations.mode([1, 1, 1, 2, 3])
        self.assertEqual(result, [1])

    def test_mode_multiple_modes(self):
        """Test mode with multiple most frequent values"""
        result = Calculations.mode([1, 1, 2, 2, 3])
        self.assertCountEqual(result, [1, 2])

    def test_mode_all_equal_frequency(self):
        """Test mode when all values have equal frequency"""
        result = Calculations.mode([1, 2, 3, 4])
        self.assertEqual(len(result), 4)

    def test_mode_with_duplicates(self):
        """Test mode with many duplicates"""
        result = Calculations.mode([1, 1, 1, 1, 2])
        self.assertEqual(result, [1])


class IndexCalculationsTest(TestCase):
    """Test index calculation methods"""

    def test_ageing_index(self):
        """Test ageing index calculation"""
        result = IndexCalculations.ageing_idx(10, 20)
        self.assertEqual(result, 0.5)

    def test_ageing_index_same_values(self):
        """Test ageing index with same values"""
        result = IndexCalculations.ageing_idx(10, 10)
        self.assertEqual(result, 1.0)

    def test_sauvy_index(self):
        """Test Sauvy index calculation"""
        result = IndexCalculations.sauvy_idx(15, 30)
        self.assertEqual(result, 0.5)

    def test_ec_weight_index(self):
        """Test economic weight index"""
        result = IndexCalculations.ec_weight_idx(100, 200, 150)
        self.assertEqual(result, 225.0)

    def test_dependency_index(self):
        """Test dependency index"""
        result = IndexCalculations.dependency_idx(50, 100)
        self.assertEqual(result, 50.0)

    def test_shadow_index(self):
        """Test shadow index"""
        result = IndexCalculations.shadow_idx(75, 100)
        self.assertEqual(result, 75.0)

    def test_multiple_indices(self):
        """Test multiple index calculations together"""
        age = IndexCalculations.ageing_idx(20, 40)
        sau = IndexCalculations.sauvy_idx(10, 15)
        self.assertEqual(age, 0.5)
        self.assertAlmostEqual(sau, 0.667, places=2)


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


class IndexCalculatorViewTest(TestCase):
    """Test index calculator view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('index_calculator')

    def test_index_calculator_get_status_code(self):
        """Test index calculator view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_calculator_view_template(self):
        """Test index calculator view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'calculator/index_calculator.html')

    def test_index_calculator_view_accessible(self):
        """Test index calculator view is accessible"""
        response = self.client.get(self.url)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)


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
