#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
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
        test_url = f"https://api.github.com/orgs/{org_name}"
        GithubOrgClient(org_name).org
        mock_get_json.assert_called_once_with(test_url)

    def test_public_repos_url(self):
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock, return_value="dummy_url") as mock_url:
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("dummy_url")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
