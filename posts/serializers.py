from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth.hashers import make_password
from .models import Post, User


class UserSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post_detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'posts', 'country')

class UserRegistrationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'country', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] == data['confirm_password']:
            return data
        raise serializers.ValidationError("Passwords do not match")

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        instance = User.objects.create_user(**validated_data)
        instance.confirm_password = make_password(confirm_password)
        return instance

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
