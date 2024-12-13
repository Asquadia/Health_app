import unittest
from unittest.mock import patch
import sys
import os

# Adjust the path to include the project root directory
test_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(test_dir)
sys.path.insert(0, project_dir)

# Import using direct module names since they are in the project root
from backend.app import app as backend_app
from bmi_service.bmi import bmi
from bmr_service.bmr import bmr

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        """Setup test client before each test."""
        self.backend_app = backend_app.test_client()
        self.backend_app.testing = True

    def print_test_info(self, service, endpoint, input_values, expected_value, returned_value):
        """Prints detailed information about the test."""
        print(f"---------------------------------------")
        print(f"Service: {service}")
        print(f"Endpoint: {endpoint}")
        print(f"Input Values: {input_values}")
        print(f"Expected Value: {expected_value}")
        print(f"Returned Value: {returned_value}")
        print(f"Test Result: {'PASSED' if returned_value == expected_value else 'FAILED'}")
        print(f"---------------------------------------")

    def test_api_calculate_bmi_success(self):
        """Test the /api/bmi endpoint with successful external API call."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858}  # Corrected expected value

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_api_calculate_bmi_missing_params(self):
        """Test the /api/bmi endpoint with missing parameters."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70}
        expected_value = {'error': 'Weight and height are required parameters.'}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_api_calculate_bmr_success(self):
        """Test the /api/bmr endpoint with successful external API call."""
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'bmr': 1695.667}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(returned_value['bmr'], expected_value['bmr'])

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_calculation(self):
        """Test the bmi function with valid inputs."""
        service = "BMI Function"
        endpoint = "N/A"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = 22.857142857142858

        returned_value = bmi(**input_values)

        self.assertAlmostEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmr_calculation(self):
        """Test the bmr function with valid inputs."""
        service = "BMR Function"
        endpoint = "N/A"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = 1695.667

        returned_value = bmr(**input_values)

        self.assertAlmostEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

if __name__ == '__main__':
    unittest.main()
