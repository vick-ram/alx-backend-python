#!/usr/bin/env python3
"""test_client module"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""

    first_url = "https://api.github.com/orgs/google/repos"
    second_url = "https://api.github.com/orgs/abc/repos"

    @parameterized.expand([
        ("google", {"login": "google", "repos_url": first_url}),
        ("abc", {"login": "abc", "repos_url": second_url}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""

        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)

        org = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(org, expected_response)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct repos_url."""
        mock_org_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
                GithubOrgClient,
                'org', return_value=mock_org_payload):
            """Instantiate the client with any org name"""
            client = GithubOrgClient("google")

            """Check if _public_repos_url returns the correct repos_url"""
            result = client._public_repos_url
            expected_url = "https://api.github.com/orgs/google/repos"

            self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos."""

        """Define the mock payload that get_json will return"""
        mock_repo_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]

        """Set the return value of the mock get_json function"""
        mock_get_json.return_value = mock_repo_payload

        """Mock the _public_repos_url property"""
        mock_url = "https://api.github.com/orgs/google/repos"
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=patch.PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_url

            """Instantiate the GithubOrgClient"""
            client = GithubOrgClient("google")

            """Call the public_repos method"""
            repos = client.public_repos()

            """Expected list of repo names"""
            expected_repos = ["repo1", "repo2", "repo3"]

            """Assert that the returned repos match the expected list"""
            self.assertEqual(repos, expected_repos)

            """Assert that _public_repos_url was called once"""
            mock_public_repos_url.assert_called_once()

            """Assert that get_json was called once with the mocked URL"""
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different scenarios."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
