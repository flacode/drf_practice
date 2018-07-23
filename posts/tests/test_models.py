from django.test import TransactionTestCase
from posts.models import User, Post


class UserModelTestCase(TransactionTestCase):
    """Test suite for custom User model"""

    reset_sequences = True

    def setUp(self):
        self.user = {
            'username': 'username',
            'password': 'password',
            'country': 'UG'
            }

    def test_user_object_creation(self):
        user = User(**self.user)
        user.save()
        created_user = User.objects.first()
        username = f'{created_user.username}'
        self.assertEqual(username, self.user['username'])

    def test_user_object_creation_with_email(self):
        self.user['email'] = 'user@gmail.com'
        user = User(**self.user)
        user.save()
        created_user = User.objects.first()
        self.assertEqual(created_user.email, self.user['email'])

class PostModelTestCase(TransactionTestCase):
    """Test suite for post model"""

    reset_sequences = True

    def setUp(self):
        self.user = {
            'username': 'username',
            'password': 'password',
            'country': 'UG'
            }
        self.post = {
            'title': 'My title',
            'content': 'My content',
            'author': User.objects.create(**self.user)
        }
        post = Post(**self.post)
        post.save()
        self.post_created = Post.objects.first()

    def test_post_creation(self):
        self.assertEqual(self.post_created.title, self.post['title'])

    def test_post_representation(self):
        self.assertEqual(self.post_created.title, str(self.post_created))
