from rest_framework import permissions

class IsListener(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == "GET":
            return True
        return False

class IsRedactorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "redactor" or request.user.role == "administrator":
            return True
        return False