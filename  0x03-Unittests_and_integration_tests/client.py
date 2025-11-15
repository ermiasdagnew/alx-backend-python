#!/usr/bin/env python3
"""GithubOrgClient class."""

import requests


class GithubOrgClient:
    """Client to interact with Github API for an organization."""

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return organization info."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return requests.get(url).json()

    @property
    def _public_repos_url(self):
        """Return public repos URL."""
        return self.org()["repos_url"]

    def public_repos(self, license=None):
        """Return list of public repos, filtered by license."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [repo["name"] for repo in repos if self.has_license(repo, license)]

    @staticmethod
    def has_license(repo, license_key):
        """Return True if repo has license."""
        return repo.get("license", {}).get("key") == license_key
