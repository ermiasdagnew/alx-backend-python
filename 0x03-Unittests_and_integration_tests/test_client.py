#!/usr/bin/env python3
"""Unit and integration tests for client.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"org": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        client = GithubOrgClient("org")
        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            self.assertEqual(client._public_repos_url, "http://example.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        client = GithubOrgClient("org")
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=property
        ) as mock_url:
            mock_url.return_value = "http://example.com/repos"
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            self.assertEqual(client.public_repos(license="mit"), ["repo1"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
