from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TransactionTestCase
from rest_framework import status


class UserRegistrationTestCase(TransactionTestCase):
    """Test for user registration view"""

    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = {
            'username': 'username',
            'country': 'Uganda',
            'password': 'password',
            'confirm_password': 'password'
        }

    def test_user_registration(self):
        response = self.client.post(reverse('register'), data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_with_optional_email(self):
        self.user['email'] = 'email@email.com'
        response = self.client.post(reverse('register'), data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_with_different_passwords(self):
        self.user['password'] = 'password123'
        response = self.client.post(reverse('register'), data=self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
