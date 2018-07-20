from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth.hashers import make_password
from .models import Post, User


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'posts', 'country')

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'country', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] == data['confirm_password']:
            return data
        raise serializers.ValidationError("Passwords do not match")

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        instance = User.objects.create(**validated_data)
        instance.confirm_password = make_password(confirm_password)
        return instance

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
