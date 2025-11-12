#!/usr/bin/env python3
"""Test utils module"""

import unittest
from unittest.mock import patch
from utils import memoize


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
