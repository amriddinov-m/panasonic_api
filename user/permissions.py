from rest_framework.permissions import BasePermission

class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'director'

class IsDealer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'dealer'

class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'provider'