#!/usr/bin/env python3
"""Utility functions."""

import requests
from functools import wraps


def access_nested_map(nested_map, path):
    """Access a nested map using a path."""
    current = nested_map
    for key in path:
        current = current[key]
    return current


def get_json(url):
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Decorator to memoize a method."""
    attr_name = "_memoized_" + fn.__name__

    @property
    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return memoized
