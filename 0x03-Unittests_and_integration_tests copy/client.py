#!/usr/bin/env python3
"""A GitHub organization client."""

from typing import List, Dict
from utils import get_json, access_nested_map, memoize


class GithubOrgClient:
    """Client to interact with the GitHub organization API."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize a GithubOrgClient with the organization name."""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Return the organization JSON payload from GitHub API.

        This method is memoized to avoid multiple HTTP requests.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the URL to access public repositories for the org."""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> List[Dict]:
        """Return the list of repositories as JSON payload.

        This method is memoized to avoid multiple HTTP requests.
        """
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Return a list of public repository names.

        Optionally filter by license key.

        Parameters
        ----------
        license : str, optional
            License key to filter repositories (default is None).

        Returns
        -------
        List[str]
            List of repository names
        """
        payload = self.repos_payload
        repos = [
            repo["name"] for repo in payload
            if license is None or self.has_license(repo, license)
        ]
        return repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if a repository has the specified license key.

        Parameters
        ----------
        repo : dict
            Repository dictionary
        license_key : str
            License key to check

        Returns
        -------
        bool
            True if the repo has the given license key, False otherwise
        """
        assert license_key is not None, "license_key cannot be None"
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
