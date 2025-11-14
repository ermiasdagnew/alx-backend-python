#!/usr/bin/env python3
"""Fixtures for testing GithubOrgClient."""

org_payload = {
    "login": "org",
    "repos_url": "http://example.com/org/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "mit"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
    {"name": "repo3", "license": {"key": "bsd"}},
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo2"]
