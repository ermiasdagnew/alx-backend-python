#!/usr/bin/env python3
"""Fixtures for integration tests of GithubOrgClient"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "events_url": "https://api.github.com/orgs/google/events",
    "hooks_url": "https://api.github.com/orgs/google/hooks",
    "issues_url": "https://api.github.com/orgs/google/issues",
    "members_url": "https://api.github.com/orgs/google/members{/member}",
    "public_members_url": "https://api.github.com/orgs/google/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/1342004?v=4",
    "description": "Google ❤️ Open Source"
}

repos_payload = [
    {
        "id": 7697149,
        "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
        "name": "episodes.dart",
        "full_name": "google/episodes.dart",
        "private": False,
        "owner": {"login": "google", "id": 1342004},
        "license": {"key": "apache-2.0", "name": "Apache License 2.0"},
    },
    {
        "id": 7776515,
        "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
        "name": "cpp-netlib",
        "full_name": "google/cpp-netlib",
        "private": False,
        "owner": {"login": "google", "id": 1342004},
        "license": {"key": "mit", "name": "MIT License"},
    },
    {
        "id": 11170671,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMTE3MDY3MQ==",
        "name": "google.github.io",
        "full_name": "google/google.github.io",
        "private": False,
        "owner": {"login": "google", "id": 1342004},
        "license": {"key": "apache-2.0", "name": "Apache License 2.0"},
    },
]

# Expected outputs for integration tests
expected_repos = ["episodes.dart", "cpp-netlib", "google.github.io"]

apache2_repos = ["episodes.dart", "google.github.io"]
