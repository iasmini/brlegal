from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('account:users')
TOKEN_URL = reverse('account:token')
ME_URL = reverse('account:me')


# helper function to create user
# **param - dynamic list of arguments
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# the instructor separates in public and private
# the public api is unauthenticated
# the private api is authenticated
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        # it simplifies to call our client in our test to not have to create it
        # manually in every single test we run
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        # the payload is the object that you pass to the api in the request
        payload = {
            'email': 'test@test.com',
            'password': '123',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # test if the object was actually created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # unwind the response - it'll take the dictionary response (similar to
        # the payload dictionary, plus id field)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # test if the password is not in the res.data, for security it
        # shouldnt be
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@test.com', 'password': '1234'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test thar the password must be more than 1 character"""
        payload = {'email': 'test@test.com', 'password': '123'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # if the user exists it will return true
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created for the user"""
        payload = {'email': 'test@test.com', 'password': '123'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        # checks that there is a key called token in the response
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com', password='1234')
        payload = {'email': 'test@test.com', 'password': 'wrong'}

        res = self.client.post(TOKEN_URL, payload)

        # checks that there is not a key called token in the response
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': '123'}

        # this time we dont create the user which is the purpose of this test

        res = self.client.post(TOKEN_URL, payload)

        # checks that there is not a key called token in the response
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'test', 'password': ''}

        # this time we dont create the user which is the purpose of this test

        res = self.client.post(TOKEN_URL, payload)

        # checks that there is not a key called token in the response
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentications"""

    def setUp(self):
        # it simplifies to call our user in our test to not have to create it
        # manually in every single test we run
        self.user = create_user(
            email='test@test.com',
            password='123',
            name='test name'
        )

        # it simplifies to call our client in our test to not have to create it
        # manually in every single test we run
        self.client = APIClient()
        # already authenticates with the created user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        # it has to be different that default user created in setup
        payload = {
            'email': 'test2@test.com',
            'password': '1234',
            'name': 'test2 name'
        }
        res = self.client.patch(ME_URL, payload)

        # we use the refresh from db helper function to update the user with
        # the latest values from the database
        self.user.refresh_from_db()

        # verify that each of the the values we provided was updated
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
