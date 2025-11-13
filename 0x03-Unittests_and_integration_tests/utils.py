#!/usr/bin/env python3
"""Generic utilities for GitHub org client."""

import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Args:
        nested_map (Mapping): A nested dictionary.
        path (Sequence): A sequence of keys representing the path.

    Returns:
        Any: The value found at the end of the path.

    Raises:
        KeyError: If a key in the path is not found.

    Example:
        >>> nested_map = {"a": {"b": {"c": 1}}}
        >>> access_nested_map(nested_map, ["a", "b", "c"])
        1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """
    Get JSON content from a remote URL.

    Args:
        url (str): URL to fetch the JSON from.

    Returns:
        Dict: Parsed JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Decorator to memoize a method’s return value.

    This ensures that subsequent calls return the cached result
    instead of re-running the method.

    Example:
        class MyClass:
            @memoize
            def a_method(self):
                print("a_method called")
                return 42

        >>> obj = MyClass()
        >>> obj.a_method
        a_method called
        42
        >>> obj.a_method
        42
    """
    attr_name = f"_{fn.__name__}"

    @wraps(fn)
    def memoized(self):
        """Cached version of the wrapped method."""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
