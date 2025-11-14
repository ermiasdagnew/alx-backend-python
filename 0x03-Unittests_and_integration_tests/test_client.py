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
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        client = GithubOrgClient("org")
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
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

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=property) as mock_url:
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


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def json_side_effect(url):
            if url.endswith("/repos"):
                return cls.repos_payload
            return cls.org_payload

        mock_get.return_value.json.side_effect = json_side_effect
        cls.client = GithubOrgClient(cls.org_payload.get("login", "org"))

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        self.assertEqual(self.client.public_repos(), self.expected_repos)
        self.assertEqual(self.client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
