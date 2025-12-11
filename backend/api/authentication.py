from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer, UserDetailSerializer
from rest_framework import serializers


"""
Custom JWT serializer that includes extra user data in the token response.

This serializer extends DRF-SimpleJWT's TokenObtainPairSerializer and:
- Adds custom claims to JWT tokens (email, name, role, profile flags).
- Implements custom validation to authenticate against the project's
  User model instead of Django's default auth.User.
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    """
    Generate a JWT refresh token with additional custom claims.

    Parameters
    ----------
    user : User
        The authenticated user for whom the token is created.

    Returns
    -------
    RefreshToken
        The generated token containing both default and custom claims.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['role'] = user.role

        # Profile flags
        token['is_admin'] = hasattr(user, 'admin_profile')
        token['is_auth_user'] = hasattr(user, 'auth_profile')

        return token

    """
    Validate user credentials using email and password.

    Parameters
    ----------
    attrs : dict
        Raw login data containing email (or username) and password.

    Returns
    -------
    dict
        Contains the refresh token, access token, and serialized user data.

    Raises
    ------
    ValidationError
        If credentials are missing or invalid.
    """
    def validate(self, attrs):
        email = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required')

        # Try to fetch user from custom User model
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        # Validate password
        if not check_password(password, user.password_hash):
            raise serializers.ValidationError('Invalid credentials')

        # Generate tokens
        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserDetailSerializer(user).data
        }


"""
Custom login endpoint using email/password.

Example:
POST /api/auth/login/
{
    "email": "user@example.com",
    "password": "password123"
}
"""
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ----------------------------------------------------------------------
# Register User
# ----------------------------------------------------------------------

"""
Register a new VRISA user.

Endpoint
--------
POST /api/auth/register/

Expected Body
-------------
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "citizen"
}

Returns
-------
201 CREATED with user info + tokens
400 BAD REQUEST if data is invalid
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserDetailSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------
# Logout
# ----------------------------------------------------------------------

"""
Logout the currently authenticated user by blacklisting a refresh token.

Endpoint
--------
POST /api/auth/logout/

Body
----
{
    "refresh": "refresh_token_here"
}
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------
# Change Password
# ----------------------------------------------------------------------

"""
Allows an authenticated user to change their password.

Endpoint
--------
POST /api/auth/change-password/

Body
----
{
    "old_password": "old_pass",
    "new_password": "new_pass"
}
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response(
            {'error': 'old_password and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate old password
    if not check_password(old_password, user.password_hash):
        return Response(
            {'error': 'Old password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update password
    from django.contrib.auth.hashers import make_password
    user.password_hash = make_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------
# Verify Token
# ----------------------------------------------------------------------

"""
Verify that the provided JWT token is valid.

Endpoint
--------
GET /api/auth/verify/

Returns
-------
{
    "valid": true,
    "user": { ... }
}
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    serializer = UserDetailSerializer(request.user)
    return Response({
        'valid': True,
        'user': serializer.data
    })