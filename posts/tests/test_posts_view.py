from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TransactionTestCase
from rest_framework import status
from posts.models import Post

class PostsTestCase(TransactionTestCase):
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
        self.user2 = {
            'username': 'username2',
            'country': 'Uganda',
            'password': 'password',
            'confirm_password': 'password'
        }
        self.client.post(reverse('register'), data=self.user2)
        self.post = {
            'title': 'My title',
            'content': 'My content'
        }


    def create_post(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        return self.client.post(reverse('post_list'), data=self.post)

    def test_create_post_when_authorised(self):
        posts_before = Post.objects.all().count()
        response = self.create_post()
        posts_after = Post.objects.all().count()
        self.assertNotEqual(posts_before, posts_after)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_when_unauthorised(self):
        response = self.client.post(reverse('post_list'), data=self.post)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_posts(self):
        self.create_post()
        response = self.client.get(reverse('post_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_posts_unauthenticated_user(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_post_by_author(self):
        self.create_post()
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_post_by_unauthenticated_user(self):
        self.create_post()
        self.client.credentials()
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_post_by_another_authenticated_user(self):
        self.create_post()
        self.client.credentials()
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_unexisting_post_by_authenticated_user(self):
        self.create_post()
        response = self.client.get(reverse('post_detail', kwargs={'pk':2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_post_by_author(self):
        self.create_post()
        response = self.client.patch(reverse('post_detail', kwargs={'pk':1}), data={'title': 'username'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_by_another_authenticated_user(self):
        self.create_post()
        self.client.credentials()
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('post_detail', kwargs={'pk':1}), data={'title': 'username'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_by_unauthenticated_user(self):
        self.create_post()
        self.client.credentials()
        response = self.client.patch(reverse('post_detail', kwargs={'pk':1}), data={'title': 'username'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_unexisting_post_by_authenticated_user(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('post_detail', kwargs={'pk':1}), data={'title': 'username'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_by_another_authenticated_user(self):
        self.create_post()
        self.client.credentials()
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(reverse('post_detail', kwargs={'pk':1}), data={'title': 'username'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_single_post_by_author(self):
        self.create_post()
        response = self.client.delete(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_by_another_authenticated_user(self):
        self.create_post()
        self.client.credentials()
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_unauthenticated_user(self):
        self.create_post()
        self.client.credentials()
        response = self.client.delete(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_unexisting_post_by_authenticated_user(self):
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_by_another_authenticated_user(self):
        self.create_post()
        self.client.credentials()
        login_data = self.client.post(reverse('login'), data={'username': 'username2', 'password': 'password'})
        token = login_data.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
