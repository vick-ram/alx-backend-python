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


if __name__ == "__main__":
    unittest.main()
