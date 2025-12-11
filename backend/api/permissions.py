from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users who have an admin_profile.

    Used for endpoints restricted exclusively to admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'admin_profile')
        )


class IsAuthUser(permissions.BasePermission):
    """
    Allows access only to users who have an auth_profile.

    Used when an authenticated non-admin user is required.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'auth_profile')
        )


class IsAdminOrAuthUser(permissions.BasePermission):
    """
    Allows access to both admin users and auth users.

    Useful for endpoints where both types of profiles are valid.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return (
            hasattr(request.user, 'admin_profile') or
            hasattr(request.user, 'auth_profile')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Grants full permissions to admin users.
    Non-admins only have read-only access (safe methods).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'admin_profile')
        )


class IsInstitutionAdmin(permissions.BasePermission):
    """
    Restricts modification of an institution to its own admin.
    Read-only access is allowed for all authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if not hasattr(request.user, 'admin_profile'):
            return False

        # Check if the user's admin profile matches the institution's admin
        return obj.admin == request.user.admin_profile


class IsStationAdmin(permissions.BasePermission):
    """
    Restricts modification of a station to:
    - the station's own admin, or
    - the admin of the institution that owns the station.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if not hasattr(request.user, 'admin_profile'):
            return False

        # Station admin or institution admin
        return (
            obj.admin == request.user.admin_profile or
            obj.institution.admin == request.user.admin_profile
        )


class CanAccessStation(permissions.BasePermission):
    """
    Controls access to station objects:

    - Admin users have full access.
    - Auth users can only access stations they've been explicitly granted
      via StationConsult.
    """

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if hasattr(request.user, 'admin_profile'):
            return True

        # Auth users need explicit access via station_consults
        if hasattr(request.user, 'auth_profile'):
            from .models import StationConsult
            return StationConsult.objects.filter(
                auth_user=request.user.auth_profile,
                station=obj
            ).exists()

        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access to:
    - Admin users (full access)
    - The owner of the object (if the object has a 'user' attribute)
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if hasattr(request.user, 'admin_profile'):
            return True

        # Users can access their own data
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False