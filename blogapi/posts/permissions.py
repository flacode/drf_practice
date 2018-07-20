from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You can not edit or delete this post'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsUserOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
