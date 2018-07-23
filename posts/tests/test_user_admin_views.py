from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TransactionTestCase
from rest_framework import status
from posts.models import User

class UserAdminTestCase(TransactionTestCase):
    """Test for the user admin views"""

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
        self.admin = {
            'username': 'admin',
            'country': 'Uganda',
            'password': 'password',
            'is_staff': 'true',
            'confirm_password': 'password'
        }
        self.client.post(reverse('register'), data=self.admin)

    def test_admin_access_to_user_list(self):
        login_data = self.client.post(reverse('login'), data={'username': 'admin', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_access_to_user_list(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_access_to_user_list(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_right_to_delete_user(self):
        login_data = self.client.post(reverse('login'), data={'username': 'admin', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        users_before_delete = User.objects.all().count()
        response = self.client.delete(reverse('user_details', kwargs={'pk':2}))
        users_after_delete = User.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(users_before_delete, users_after_delete)

    def test_public_right_to_delete_user(self):
        users_before_delete = User.objects.all().count()
        response = self.client.delete(reverse('user_details', kwargs={'pk':2}))
        users_after_delete = User.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(users_before_delete, users_after_delete)

    def test_non_admin_right_to_delete_user(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        users_before_delete = User.objects.all().count()
        response = self.client.delete(reverse('user_details', kwargs={'pk':2}))
        users_after_delete = User.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(users_before_delete, users_after_delete)
