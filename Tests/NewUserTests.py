import random
import unittest
import json

import requests
from rest_framework import status

from BloodBankWebApp.StringUtils import bloodGroups, cityNames, address, randomNames, randomStrongPasswords, \
    user_token_key, user_id_key, user_details_url
from Tests.AccessTests import protocols


def phone_generator() -> str:
    phone = "0"
    for times in range(10):
        num = random.choice(range(10))
        phone += str(num)
    return phone


random_name_generator = lambda: random.choice(randomNames)
blood_group_choicer = lambda: random.choice(bloodGroups)
city_name_generator = lambda: random.choice(cityNames)
sudan_address_generator = lambda: random.choice(address)
random_strong_password_generator = lambda: random.choice(randomStrongPasswords)


def isSameUser(subset, dictionary):
    # TODO: Come on! You know that won't work!
    return (set(subset.items()).issubset(set(dictionary.items())))


def hasToken(user):
    if user_token_key in user:
        return True
    return False


def getUserFromResponse(response):
    return json.loads(response.text)


def createRandomUser() -> dict:
    user = {
        "username": random_name_generator(),
        "password": random_strong_password_generator(),
        "phone": phone_generator(),
        "bloodGroup": blood_group_choicer(),
        "city": city_name_generator(),
        "address": sudan_address_generator()}
    return user


def updatedUserDetails(user):
    return user


class UsersAuthorization(unittest.TestCase):
    lastUser = dict()
    lastUserToken = None

    def test_create_new_user(self):
        testUser = createRandomUser()
        for protocol in protocols:
            url = protocol + user_details_url
            response = requests.put(url, data=testUser)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            createdUser = getUserFromResponse(response)
            self.assertTrue(isSameUser(testUser, createdUser))
            self.assertTrue(hasToken(createdUser))
            self.storeUser(createdUser)

    def test_retrieve_user_details_without_token(self):
        localUser = self.getUser()
        url = f"{user_details_url}/{localUser[user_id_key]}"
        response = requests.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_details_token(self):
        localUser = self.getUser()
        url = f"{user_details_url}/{localUser[user_id_key]}"
        tokenHead = {'Authorization': f'token {self.getToken()}'}
        response = requests.get(url, headers=tokenHead)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        remoteUser = getUserFromResponse(response)
        self.assertTrue(isSameUser(remoteUser, localUser))
        self.storeUser(remoteUser)

    def test_update_details(self):
        localUser = self.getUser()
        updatedUser = updatedUserDetails(localUser)
        url = f"{user_details_url}/{localUser[user_id_key]}"
        tokenHead = {'Authorization': f'token {self.getToken()}'}
        response = requests.put(url, headers=tokenHead, data=updatedUser)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.test_retrieve_user_details_token()
        localUser = self.getUser()
        self.assertTrue(isSameUser(localUser, updatedUser))

    def getUser(self):
        if self.lastUserToken is not None:
            return self.lastUser
        else:
            # TODO: Ask for new Token instead of creating new user if there is user
            self.test_create_new_user()
            return self.lastUser

    def storeUser(self, user):
        if hasToken(user):
            self.lastUserToken = user[user_token_key]
        self.lastUser = user

    def getToken(self):
        return self.lastUserToken


if __name__ == '__main__':
    unittest.main()
    # TODO: Track test users and delete them after finish
