#!/usr/bin/env python3
"""Test client module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        client = GithubOrgClient("test")
        client.org = {"repos_url": "http://fake.url"}
        self.assertEqual(client._public_repos_url, "http://fake.url")

    @patch("client.get_json")
    def test_repos_payload(self, mock_get_json):
        """Test repos_payload property"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test")
        client._public_repos_url = "http://fake.url"
        self.assertEqual(client.repos_payload, [{"name": "repo1"}, {"name": "repo2"}])
        mock_get_json.assert_called_once_with("http://fake.url")

    def test_public_repos(self):
        """Test public_repos method with license filtering"""
        client = GithubOrgClient("test")
        client.repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "bsd-3-clause"}},
            {"name": "repo3"},
        ]
        # No license filter
        self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
        # License filter
        self.assertEqual(client.public_repos("apache-2.0"), ["repo1"])
        self.assertEqual(client.public_repos("bsd-3-clause"), ["repo2"])

    def test_has_license(self):
        """Test has_license static method"""
        repo = {"license": {"key": "apache-2.0"}}
        self.assertTrue(GithubOrgClient.has_license(repo, "apache-2.0"))
        self.assertFalse(GithubOrgClient.has_license(repo, "bsd-3-clause"))
        # Repo without license key
        self.assertFalse(GithubOrgClient.has_license({}, "apache-2.0"))


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures"""

    @patch("client.get_json")
    def test_integration_public_repos(self, mock_get_json):
        """Test public_repos end-to-end using fixtures"""
        # First call returns org_payload, second call returns repos_payload
        mock_get_json.side_effect = [org_payload, repos_payload]

        client = GithubOrgClient("google")
        self.assertEqual(client.org, org_payload)
        self.assertEqual(client.repos_payload, repos_payload)
        self.assertEqual(
            client.public_repos(),
            [repo["name"] for repo in repos_payload]
        )
        # License filtering works
        license_key = repos_payload[0]["license"]["key"]
        self.assertEqual(client.public_repos(license_key), [repos_payload[0]["name"]])
        # get_json called twice: org + repos
        self.assertEqual(mock_get_json.call_count, 2)


if __name__ == "__main__":
    unittest.main()
