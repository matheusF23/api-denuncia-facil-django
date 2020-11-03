from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@x9.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email, f"user.email must be '{email}'")
        self.assertTrue(user.check_password(password), "password must be ok")

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@X9.COM'
        user = get_user_model().objects.create_user(email, 'testpass')

        self.assertEqual(user.email, email.lower(),
                         "user.email must be normalized")

    def test_new_invalid_email(self):
        """Test creating a new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_complete_user_model(self):
        """Test creating a new user with all fields"""
        payload = {
            'name': "complete user name",
            "cellphone": "98977777777",
        }
        user = get_user_model().objects.create_user(
            email='user@x9.com',
            **payload
        )
        self.assertEqual(user.get_full_name(), payload['name'],
                         'must get full name of user')
        self.assertEqual(user.get_short_name(), 'complete',
                         'must get first name of user')
        self.assertEqual(str(user), user.email, 'str user must return the email')
        for key in payload.keys():
            self.assertEqual(
                payload[key], getattr(user, key),
                f'{key}, must be {payload[key]}'
            )

    def test_user_with_existing_email(self):
        get_user_model().objects.create_user(email="user@x9.com")
        with self.assertRaises(Exception) as context:
            get_user_model().objects.create_user("user@x9.com")
        self.assertTrue('UNIQUE constraint failed: accounts_user.email' in str(context.exception),
                        'must rise that email must be unique')

    def test_user_no_name(self):
        user = get_user_model().objects.create_user(email="user@x9.com")
        self.assertEqual(None, user.get_full_name(),
                         'None must be returned if user no have name')
        self.assertEqual(None, user.get_short_name(),
                         'None must be returned if user no have name')


class SuperUserModelTests(TestCase):

    def test_create_superuser(self):
        """Test creating a new superuser"""
        superuser = get_user_model().objects.create_superuser(
            'super@x9.com',
            'testpass'
        )
        self.assertTrue(superuser.is_superuser, 'must return True for a superuser')
        self.assertTrue(superuser.is_staff, 'must return True for a superuser')
