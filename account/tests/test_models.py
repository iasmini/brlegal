from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = '123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for a new user is normalized. The second part of
        user domain name for email addresses is case-insensitive. It makes that
        part all lowercase when registering a new user"""
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, '123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # anything that run in here should raise an error. if dont, this test
        # failed
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            '123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
