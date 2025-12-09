from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User


class CustomUserBackend(BaseBackend):
    """
    Custom authentication backend for VRISA User model.
    Authenticates using email instead of username.
    """
    
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        """
        Authenticate user by email and password.
        """
        # Accept either 'username' or 'email' parameter
        email = email or username
        
        if not email or not password:
            return None
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        # Check password
        if check_password(password, user.password_hash):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None