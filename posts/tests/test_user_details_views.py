from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TransactionTestCase
from rest_framework import status


class UserViewTestCase(TransactionTestCase):
    """Test for user details view"""

    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = {
            'username': 'username',
            'country': 'Uganda',
            'password': 'password',
            'confirm_password': 'password'
        }
        self.client.post(reverse('register'), data=self.user)

    def test_user_view_for_their_details(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('user_view', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_view_for_another_users_details(self):
        user = {
            'username': 'username1',
            'country': 'Uganda',
            'password': 'password',
            'confirm_password': 'password'
        }
        self.client.post(reverse('register'), data=user)
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('user_view', kwargs={'pk':2}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_access_to_user_details(self):
        response = self.client.get(reverse('user_view', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_view_with_unexisting_user(self):
        response = self.client.get(reverse('user_view', kwargs={'pk':2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_details_for_own_account(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('user_view', kwargs={'pk':1}), data={'username': 'username'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_not_update_another_users_account_details(self):
        user = {
            'username': 'username1',
            'country': 'Uganda',
            'password': 'password',
            'confirm_password': 'password'
        }
        self.client.post(reverse('register'), data=user)
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('user_view', kwargs={'pk':2}), data={'username': 'username'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_access_to_update_user_details(self):
        response = self.client.patch(reverse('user_view', kwargs={'pk':1}), data={'username': 'username'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_details_update_with_unexisting_user(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('user_view', kwargs={'pk':9}), data={'username': 'username'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
