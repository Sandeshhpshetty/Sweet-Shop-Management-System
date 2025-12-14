from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.is_admin
        )
    def get_permissions(self):
        if self.action in ["destroy", "restock", "destock"]:
            return [IsAdmin()]  # Admin only actions
        return [permissions.IsAuthenticated()]