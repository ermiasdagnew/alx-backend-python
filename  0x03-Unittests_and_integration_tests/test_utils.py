#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map  # make sure utils.py has this function


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({}, ("a",)),                # empty dict, key "a" missing
        ({"a": 1}, ("a", "b")),      # dict with only key "a", but path includes "b"
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised with proper message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check if KeyError message matches the missing key
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")
