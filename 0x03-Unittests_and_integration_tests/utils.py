#!/usr/bin/env python3
"""Generic utilities for GitHub org client."""

import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable

__all__ = ["access_nested_map", "get_json", "memoize"]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map using a sequence of keys.

    Parameters
    ----------
    nested_map : Mapping
        The dictionary or mapping to access
    path : Sequence
        Sequence of keys representing the path to the desired value

    Returns
    -------
    Any
        The value found at the nested path

    Raises
    ------
    KeyError
        If any key in the path is not present in the nested map

    Example
    -------
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
    """Get JSON data from a URL using HTTP GET.

    Parameters
    ----------
    url : str
        The URL to fetch

    Returns
    -------
    dict
        The JSON payload of the response

    Example
    -------
    >>> get_json("http://example.com")
    {'payload': True}
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> property:
    """Decorator to memoize a method’s result as a property.

    Parameters
    ----------
    fn : Callable
        The instance method to memoize

    Returns
    -------
    property
        A property that caches the method's result after first call

    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            return 42

    >>> obj = MyClass()
    >>> obj.a_method
    42
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
