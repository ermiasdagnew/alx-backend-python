#!/usr/bin/env python3
"""Utility functions for accessing nested maps."""


def access_nested_map(nested_map, path):
    """Access a nested map with a sequence of keys."""
    current = nested_map
    for key in path:
        current = current[key]
    return current
