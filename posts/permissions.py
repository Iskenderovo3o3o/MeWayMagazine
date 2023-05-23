from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user


class CustomPermission(BasePermission):  # Renamed the class to CustomPermission
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and (request.user == obj.author or request.user.is_staff):  # Added parentheses for correct logical evaluation
            return True
        else:
            return False
