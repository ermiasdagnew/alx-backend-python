#!/usr/bin/env python3
"""Fixtures for GithubOrgClient integration tests."""

# Example organization payload
org_payload = {
    "login": "holberton",
    "id": 123,
    "repos_url": "https://api.github.com/orgs/holberton/repos"
}

# Example repositories payload
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]

# Expected repository names for public_repos() without license filter
expected_repos = ["repo1", "repo2", "repo3"]

# Expected repository names for public_repos(license="apache-2.0")
apache2_repos = ["repo1", "repo3"]
