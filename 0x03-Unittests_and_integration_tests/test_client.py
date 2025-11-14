#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos using fixtures."""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures

@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and start the client."""
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
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos."""
        self.assertEqual(self.client.public_repos(), self.expected_repos)
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"), self.apache2_repos
        )
