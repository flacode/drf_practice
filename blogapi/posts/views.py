from django.shortcuts import render
from .serializers import PostSerializer, UserSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from .models import Post, User
from .permissions import IsOwnerOrReadOnly, IsUserOnly


class PostList(generics.ListCreateAPIView):
    """
        Private: Authenticated user can view all posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Private: Edit and delete rights are only reserved for the author of the post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class UserList(generics.ListAPIView):
    """
        Private: Administrator/staff can view a list of available users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserAdministration(generics.RetrieveDestroyAPIView):
    """
        Private: Administator can retrieve and delete a particular user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserRegistration(generics.CreateAPIView):
    """
        Public: User can create an account
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(generics.RetrieveUpdateAPIView):
    """
        Private: Allow a user to view their details and update them
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOnly, )
