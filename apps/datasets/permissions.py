from rest_framework.permissions import BasePermission


class CanReplaceDataset(BasePermission):
    message = "Sign in with a staff or provider account to update the dataset."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {"administrator", "employee", "client"}
        )
