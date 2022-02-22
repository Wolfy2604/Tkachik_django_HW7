from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def __init__(self):
        print('OWNER')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator