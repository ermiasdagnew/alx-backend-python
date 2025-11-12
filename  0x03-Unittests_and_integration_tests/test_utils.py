#!/usr/bin/env python3
"""Test utils module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map function"""

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised with correct key for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), str(expected_key))

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test normal access_nested_map behavior"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


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


class TestMemoize(unittest.TestCase):
    """Test memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches result and calls the method only once"""

        class TestClass:
            """A class with a method to be memoized"""

            def a_method(self):
                """Method to return a fixed value"""
                return 42

            @memoize
            def a_property(self):
                """Memoized property"""
                return self.a_method()

        test_obj = TestClass()

        # Patch a_method to track calls
        with patch.object(test_obj, "a_method", wraps=test_obj.a_method) as mock_method:
            # First access calls a_method
            result1 = test_obj.a_property
            # Second access returns cached value
            result2 = test_obj.a_property

            # Assert the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # a_method should have been called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
