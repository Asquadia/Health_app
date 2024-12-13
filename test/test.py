import unittest
import requests
from unittest.mock import patch, MagicMock
import sys
import os

# Grab le directory
test_dir = os.path.dirname(os.path.abspath(__file__))
# /
project_dir = os.path.dirname(test_dir)
# sys
sys.path.insert(0, project_dir)

# import
from backend.app import app as backend_app
from bmi_service.bmi import app as bmi_service_app
from bmr_service.bmr import app as bmr_service_app


class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        """Setup test client before each test."""
        self.backend_app = backend_app.test_client()
        self.backend_app.testing = True
        self.bmi_service_app = bmi_service_app.test_client()
        self.bmi_service_app.testing = True
        self.bmr_service_app = bmr_service_app.test_client()
        self.bmr_service_app.testing = True

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

    @patch('requests.get')
    def test_api_calculate_bmi_success(self, mock_get):
        """Test the /api/bmi endpoint with successful external API call."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_value
        mock_get.return_value = mock_response

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_called_once_with(f'http://localhost:5001/bmi?weight={input_values["weight"]}&height={input_values["height"]}')

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmi_missing_params(self, mock_get):
        """Test the /api/bmi endpoint with missing parameters."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70}
        expected_value = {'error': 'Weight and height are required parameters.'}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_not_called()

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmr_success(self, mock_get):
        """Test the /api/bmr endpoint with successful external API call."""
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'bmr': 1796.439}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_value
        mock_get.return_value = mock_response

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_called_once_with(f'http://localhost:5002/bmr?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_endpoint_success(self):
        """Test the /bmi endpoint with valid inputs."""
        service = "BMI Service"
        endpoint = "/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858}

        response = self.bmi_service_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)


if __name__ == '__main__':
    unittest.main()
