from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Only users with admin_profile can access"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'admin_profile')
        )


class IsAuthUser(permissions.BasePermission):
    """Only users with auth_profile can access"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'auth_profile')
        )


class IsAdminOrAuthUser(permissions.BasePermission):
    """Admin or AuthUser can access"""
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return (
            hasattr(request.user, 'admin_profile') or 
            hasattr(request.user, 'auth_profile')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admins can edit, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'admin_profile')
        )


class IsInstitutionAdmin(permissions.BasePermission):
    """Only the admin of the institution can modify it"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not (request.user and request.user.is_authenticated):
            return False
        
        if not hasattr(request.user, 'admin_profile'):
            return False
        
        # Check if user's admin profile matches the institution's admin
        return obj.admin == request.user.admin_profile


class IsStationAdmin(permissions.BasePermission):
    """Only the station's admin can modify it"""
    
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
    """Auth users can only access stations they have been granted access to"""
    
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
    """User can access their own data, admins can access all"""
    
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if hasattr(request.user, 'admin_profile'):
            return True
        
        # Users can access their own data
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False