from rest_framework.permissions import BasePermission


class CanReplaceDataset(BasePermission):
    message = "Only staff can replace the shared dataset during the blob migration stage."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {"administrator", "employee"}
        )
