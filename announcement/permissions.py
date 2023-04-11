from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Нет доспупа для совершения действий'
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user

    