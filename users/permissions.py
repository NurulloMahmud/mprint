from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Custom permission to only allow users of the management role to access the view.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            # Checking if the user's role is "admin"
            return request.user.role.lower() == 'admin'
        except:
            # If the role relation does not exist, deny permission
            return False
