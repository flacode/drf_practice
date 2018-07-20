from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from .models import Post, User


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'posts', 'country')

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
