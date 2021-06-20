from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class AdminAccessPermission(permissions.BasePermission):
    message = "Method not allowed."

    def has_permission(self, request, view):
        return request.user.is_admin


class CurrentUserPermission(permissions.BasePermission):
    message = "Method is allowed only for current user."

    def has_permission(self, request, view):
        return (
            request.parser_context["kwargs"].get("user_id", request.user.id)
            == request.user.id
        )
