from rest_framework import serializers
from .models import Post, User

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'posts')

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
