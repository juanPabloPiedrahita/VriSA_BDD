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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with user data in response.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['role'] = user.role
        
        # Add profile flags
        token['is_admin'] = hasattr(user, 'admin_profile')
        token['is_auth_user'] = hasattr(user, 'auth_profile')
        
        return token
    
    def validate(self, attrs):
        # Custom validation using User model (not Django's auth.User)
        email = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError('Email and password are required')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        
        # Check password
        if not check_password(password, user.password_hash):
            raise serializers.ValidationError('Invalid credentials')
        
        # Generate tokens
        refresh = self.get_token(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserDetailSerializer(user).data
        }


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view using email/password.
    POST /api/auth/login/
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user.
    POST /api/auth/register/
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "citizen"
    }
    """
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting refresh token.
    POST /api/auth/logout/
    {
        "refresh": "refresh_token_here"
    }
    """
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password.
    POST /api/auth/change-password/
    {
        "old_password": "old_pass",
        "new_password": "new_pass"
    }
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {'error': 'old_password and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify old password
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify that token is valid and return user data.
    GET /api/auth/verify/
    """
    serializer = UserDetailSerializer(request.user)
    return Response({
        'valid': True,
        'user': serializer.data
    })


# Missing import
from rest_framework import serializers