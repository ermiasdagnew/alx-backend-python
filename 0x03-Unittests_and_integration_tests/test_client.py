#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        client = GithubOrgClient(org_name)
        client.org()
        mock_get.assert_not_called()

    def test_public_repos_url(self):
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "org", return_value=org_payload):
            self.assertEqual(client._public_repos_url, org_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get):
        client = GithubOrgClient("test")
        mock_get.return_value = repos_payload
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=property):
            result = client.public_repos()
            self.assertEqual(result, [repo["name"] for repo in repos_payload])
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        patcher = patch("client.requests.get")
        cls.get_patcher = patcher.start()
        cls.get_patcher.side_effect = lambda url: type(
            "obj", (), {"json": lambda: repos_payload if "repos" in url else org_payload}
        )()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
