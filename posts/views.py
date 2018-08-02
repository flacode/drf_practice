from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, User
from .permissions import IsOwnerOrReadOnly, IsCreatorOnly
from .serializers import PostSerializer, UserSerializer, UserRegistrationSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'useradmin': reverse('user_list'),
        'register': reverse('register'),
        'login': reverse('login'),
        'posts': reverse('post_list')
    })

class PostList(generics.ListCreateAPIView):
    """
        Private: Unauthenticated user can only view all posts
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


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
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message':"user account successfully created"}, status=status.HTTP_201_CREATED, headers=headers)


class UserView(generics.RetrieveUpdateAPIView):
    """
        Private: Allow a user to only view their details and update them
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreatorOnly, )
