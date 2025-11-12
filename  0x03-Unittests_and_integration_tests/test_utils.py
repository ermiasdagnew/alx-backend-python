#!/usr/bin/env python3
"""Test utils module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Test get_json function"""

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """Test that get_json calls requests.get and returns the JSON"""
        # Configure the mock to return a response with our test_payload
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        # Call the function
        result = get_json(test_url)

        # Check that requests.get was called exactly once with the test_url
        mock_get.assert_called_once_with(test_url)

        # Check that get_json returns the expected payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
