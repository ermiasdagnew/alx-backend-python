#!/usr/bin/env python3
"""Test client module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures"""

    @classmethod
    def setUpClass(cls):
        """Start patcher and configure mocked requests.get"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        # side_effect returns different payloads based on URL
        def get_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/repos"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = cls.org_payload
            return mock_resp

        mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns correct list of repo names"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
