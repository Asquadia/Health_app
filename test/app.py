import unittest
import requests
from unittest.mock import patch, MagicMock
import sys
import os

# Get the directory containing this test script (test/)
test_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from test/)
project_dir = os.path.dirname(test_dir)
# Add the project root directory to sys.path
sys.path.insert(0, project_dir)

# Import the app modules from each service
from backend.app import app as backend_app
from bmi_service.app import app as bmi_service_app
from bmr_service.app import app as bmr_service_app

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
        # Arrange
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_value
        mock_get.return_value = mock_response

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_called_once_with(f'http://localhost:5001/bmi?weight={input_values["weight"]}&height={input_values["height"]}')

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmi_missing_params(self, mock_get):
        """Test the /api/bmi endpoint with missing parameters."""
        # Arrange
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70}
        expected_value = {'error': 'Weight and height are required parameters.'}

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_not_called()

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmi_error_response(self, mock_get):
        """Test the /api/bmi endpoint with error response from external API."""
        # Arrange
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'error': 'Error contacting BMI service: Test Error'}

        mock_get.side_effect = requests.exceptions.RequestException('Test Error')

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(returned_value, expected_value)

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmr_success(self, mock_get):
        """Test the /api/bmr endpoint with successful external API call."""
        # Arrange
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'bmr': 1796.439}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_value
        mock_get.return_value = mock_response

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_called_once_with(f'http://localhost:5002/bmr?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmr_missing_params(self, mock_get):
        """Test the /api/bmr endpoint with missing parameters."""
        # Arrange
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30}
        expected_value = {'error': 'Weight, height, age, and gender are required parameters.'}

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)
        mock_get.assert_not_called()

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    @patch('requests.get')
    def test_api_calculate_bmr_error_response(self, mock_get):
        """Test the /api/bmr endpoint with error response from external API."""
        # Arrange
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'error': 'Error contacting BMR service: Test Error'}

        mock_get.side_effect = requests.exceptions.RequestException('Test Error')

        # Act
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(returned_value, expected_value)

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_endpoint_success(self):
        """Test the /bmi endpoint with valid inputs."""
        # Arrange
        service = "BMI Service"
        endpoint = "/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858}

        # Act
        response = self.bmi_service_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmi', returned_value)
        self.assertEqual(returned_value, expected_value)  # Check if returned value matches expected

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_endpoint_invalid_input(self):
        """Test the /bmi endpoint with invalid inputs."""
        # Arrange
        service = "BMI Service"
        endpoint = "/bmi"
        input_values = {'weight': -70, 'height': 1.75}
        expected_value = {'error': 'Weight and height must be positive values.'}

        # Act
        response = self.bmi_service_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmr_endpoint_success(self):
        """Test the /bmr endpoint with valid inputs."""
        # Arrange
        service = "BMR Service"
        endpoint = "/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'bmr': 1695.6670000000001}

        # Act
        response = self.bmr_service_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmr', returned_value)
        self.assertEqual(returned_value, expected_value)  # Check if returned value matches expected

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmr_endpoint_invalid_gender(self):
        """Test the /bmr endpoint with invalid gender."""
        # Arrange
        service = "BMR Service"
        endpoint = "/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'unknown'}
        expected_value = {'error': 'Invalid gender. Please specify "male" or "female".'}

        # Act
        response = self.bmr_service_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)

        # Print test info
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

if __name__ == '__main__':
    unittest.main()
