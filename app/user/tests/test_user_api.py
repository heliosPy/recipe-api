from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the users api public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucess(self):
        """Test creating user with valid payload is sucessfull"""
        payload= {
              "email":'test@londaon.com',
              "password":"testpass",
              "name": 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating user already exist fails"""
        payload = {"email":'test@londaon.com', "password":'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that the password must more than 5 characters"""
        payload = {'email': "testus@gmail.com", "password":'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """test that a token is created for the user"""
        payload = { "email": "testuser@gmail.com", 'password':'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ test that token is not created if invalid crediential are given"""
        create_user(email='test@gamil.com', password='password')
        payload={'email':'test@gamil.com', 'password':'wornge'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that token is not created if user does't exist"""
        payload={'email':'test@gamil.com', 'password':'wornge'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password is required"""
        res = self.client.post(TOKEN_URL, {'email':'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
