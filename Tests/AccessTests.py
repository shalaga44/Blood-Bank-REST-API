import unittest
import requests
from rest_framework import status

from BloodBankWebApp.StringUtils import ViewSets_urls, protocols, admin_username, admin_password


class AdminTests(unittest.TestCase):
    def test_admin_can_access_viewsets(self):
        for viewSet_url in ViewSets_urls.values():
            for protocol in protocols:
                url = f"{protocol}{admin_username}:{admin_password}@{viewSet_url}"
                admin_response = requests.get(url)
                self.assertEqual(admin_response.status_code, status.HTTP_200_OK)


class UserTests(unittest.TestCase):
    def test_user_cant_access_viewsets(self):
        for viewSet_url in ViewSets_urls.values():
            for protocol in protocols:
                url = protocol + viewSet_url
                user_response = requests.get(url)
                self.assertEqual(user_response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
