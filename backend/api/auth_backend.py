from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User

"""
Custom authentication backend for the VRISA platform.

This backend enables authentication using the email field instead
of Django's default username. It integrates with Django's
authentication system and retrieves users from the custom User model.
"""
class CustomUserBackend(BaseBackend):

    """
    Attempts to authenticate a user using their email and password.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request during the authentication attempt.
    username : str, optional
        Provided username; treated as email if 'email' is not supplied.
    email : str, optional
        Email used for authentication.
    password : str, optional
        The user's raw password.
    **kwargs :
        Additional parameters passed by Django's authentication system.

    Returns
    -------
    User or None
        Returns the authenticated User instance if credentials are valid.
        Returns None if authentication fails.
    """
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
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

    """
    Retrieve a User instance by its primary key.

    Parameters
    ----------
    user_id : int
        The ID of the user to retrieve.

    Returns
    -------
    User or None
        Returns the corresponding User instance if it exists.
        Returns None if no user is found.
    """
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
