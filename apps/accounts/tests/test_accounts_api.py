from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.accounts.api.viewsets import missing_fields


REGISTER_USER_URL = reverse('accounts-register')
LOGIN_URL = reverse('accounts-login')
UPDATE_URL = reverse('accounts-updateprofile')


def sample_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_register_valid_user_success(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'test@x9.com',
            'password': 'testpass'
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         "status code must be 201 CREATED")

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']),
                        "password must be ok")
        self.assertNotIn('password', res.data,
                         "password must not be in res.data")
        self.assertNotEqual(None, res.data['token'],
                            'token must not be None')

    def test_full_register_valid_user_success(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'test@x9.com',
            'password': 'testpass',
            'name': 'user name',
            'cellphone': '99999999999'
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         "status code must be 201 CREATED")

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']),
                        "password must be ok")
        self.assertNotIn('password', res.data,
                         "password must not be in res.data")
        self.assertNotEqual(None, res.data['token'],
                            'token must not be None')
        payload.pop('password')
        for key, value in payload.items():
            self.assertEqual(res.data[key], value,
                             'payload must be equalSim')

    def test_register_existing_user(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@x9.com',
            'password': 'testpass'
        }
        sample_user(**payload)

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT,
                         'status code must be 409 CONFLICT')

    def test_register_no_email(self):
        """Test creating user with out email"""
        payload = {'password': 'testpass'}

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         'status code must be 400 BAD REQUEST')

    def test_register_no_password(self):
        """Test creating  user with out password"""
        payload = {'email': 'test@x9.com'}
        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         "status code must be 400 BAD REQUEST")

    def test_login_success(self):
        """Test user login"""
        payload = {
            'email': 'test@x9.com',
            'password': 'testpass'
        }
        user = sample_user(**payload)
        res = self.client.post(LOGIN_URL, payload)
        token, created = Token.objects.get_or_create(user=user)

        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         "status code must be 200 OK")
        self.assertIn('token', res.data, 'token must be in response')
        self.assertEqual(res.data['name'], user.name)
        self.assertEqual(res.data['email'], user.email)
        self.assertEqual(res.data['token'], token.key)

    def test_login_fail(self):
        """Test failing user login"""
        payload = {
            'email': 'test@x9.com',
            'password': 'testpass'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         'status code must be 400 BAD REQUEST')
        self.assertNotIn('token', res.data, 'token must not be in res.data')

    def test_login_no_email(self):
        """Test make login no email"""
        payload = dict(password='testpass')
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         "status code must be 400 BAD REQUEST")

    def test_login_no_password(self):
        """Test make login no password"""
        payload = dict(email='test@x9.com')
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         "status code must be 400 BAD REQUEST")

    def test_missing_fields(self):
        data = dict(a=1, b=2, c=4)
        fields = ['a', 'b', 'c']
        is_missing, _ = missing_fields(data, *fields)
        self.assertEqual(is_missing, False)

        fields.append('d')
        is_missing, field = missing_fields(data, *fields)
        self.assertEqual((is_missing, field), (True, 'd'))


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = sample_user(
            email='test@x9.com',
            password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = dict(
            name="Other Name",
            cellphone="98745345"
        )

        res = self.client.put(UPDATE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         'status_code must be 200')
        self.assertIn(payload['name'], self.user.name,
                      f"name must be {payload['name']}")
        self.assertIn(payload['cellphone'], self.user.cellphone,
                      f"cellphone must be {payload['cellphone']}")

    def test_update_user_email(self):
        """Test updating the email of user profile for authenticated user"""
        payload = dict(
            email="otheremail@x9.com"
        )

        res = self.client.put(UPDATE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         'status_code must be 400')

    def test_update_user_password(self):
        """Test updating the password of user profile for authenticated user"""
        payload = dict(
            password="asdfasdf"
        )

        res = self.client.put(UPDATE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST,
                         'status_code must be 400')
