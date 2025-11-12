#!/usr/bin/env python3
"""Test utils module"""

import unittest
from unittest.mock import patch
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

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test that get_json calls requests.get and returns JSON"""
        mock_get.return_value.json.return_value = {"payload": True}
        url = "http://example.com"
        self.assertEqual(get_json(url), {"payload": True})
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches result and calls method only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()
        with patch.object(test_obj, "a_method", wraps=test_obj.a_method) as mock_method:
            # First access calls a_method
            self.assertEqual(test_obj.a_property, 42)
            # Second access returns cached value
            self.assertEqual(test_obj.a_property, 42)
            # Method should have been called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
