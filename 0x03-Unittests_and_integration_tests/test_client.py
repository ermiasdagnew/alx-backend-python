#!/usr/bin/env python3
"""Unit and integration tests for client.py"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org() method returns correct payload"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org()
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        client = GithubOrgClient("holberton")
        with patch.object(
            GithubOrgClient, "org", new_callable=Mock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/holberton/repos"}
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/holberton/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo list"""
        client = GithubOrgClient("holberton")
        mock_get_json.return_value = repos_payload
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=Mock
        ) as mock_url:
            mock_url.return_value = "url"
            self.assertEqual(client.public_repos(), [repo["name"] for repo in repos_payload])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        get_patcher = patch("client.requests.get", side_effect=cls.mocked_requests)
        cls.mock_get = get_patcher.start()
        cls.get_patcher = get_patcher

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests(url, *args, **kwargs):
        """Mocked requests.get().json() behavior"""
        mock_resp = Mock()
        if url == org_payload["repos_url"]:
            mock_resp.json.return_value = repos_payload
        elif url.startswith("https://api.github.com/orgs/"):
            mock_resp.json.return_value = org_payload
        else:
            mock_resp.json.return_value = {}
        return mock_resp

    def test_public_repos(self):
        """Integration test for public_repos()"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
