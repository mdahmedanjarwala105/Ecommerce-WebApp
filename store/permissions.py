from rest_framework import permissions


class IsAdminorReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users who are the staffs to read.
    Unauthenticated users will not be able to access the view.
    """

    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Deny access for non-authenticated users
        return bool(request.user and request.user.is_staff)


class ViewCustomerHistoryPermission(permissions.BasePermission):
    """
    Custom permission to allow only the customer to view their own history.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("store.view_history")
