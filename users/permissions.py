from rest_framework import permissions



class RoleBasedPermission(permissions.BasePermission):
    """
    Base permission class that accepts a list of roles to check against.
    """
    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Ensure that required_roles is not empty
        if not self.required_roles:
            raise ValueError("The required_roles attribute must be defined with at least one role.")

        # Check if the user role attribute is available
        user_role = getattr(request.user, 'role', '').lower()
        return user_role in self.required_roles


class IsAdminRole(RoleBasedPermission):
    """
    Custom permission to only allow users with the "admin" role to access the view.
    """
    required_roles = ['admin']


class IsManagerRole(RoleBasedPermission):
    """
    Custom permission to only allow users with the "manager" role to access the view.
    """
    required_roles = ['manager', 'admin']
