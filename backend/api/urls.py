from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserViewSet,
    AdminViewSet,
    AuthUserViewSet,
    InstitutionViewSet,
    StationViewSet,
    DeviceViewSet,
    AlertViewSet,
    AlertPollutantViewSet,
    AlertReceiveViewSet,
    StationConsultViewSet,
)
from .authentication import (
    CustomTokenObtainPairView,
    register_user,
    logout_user,
    change_password,
    verify_token,
)

# Create router and register viewsets
router = DefaultRouter()

# Register all viewsets
router.register(r'users', UserViewSet, basename='user')
router.register(r'admins', AdminViewSet, basename='admin')
router.register(r'auth-users', AuthUserViewSet, basename='authuser')
router.register(r'institutions', InstitutionViewSet, basename='institution')
router.register(r'stations', StationViewSet, basename='station')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'alert-pollutants', AlertPollutantViewSet, basename='alertpollutant')
router.register(r'alert-receives', AlertReceiveViewSet, basename='alertreceive')
router.register(r'station-consults', StationConsultViewSet, basename='stationconsult')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register_user, name='register'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/change-password/', change_password, name='change_password'),
    path('auth/verify/', verify_token, name='verify_token'),
    
    # Include router URLs
    path('', include(router.urls)),
]

"""
API Endpoints Summary:

Authentication:
- POST   /api/auth/login/            - Login (get access + refresh tokens)
- POST   /api/auth/refresh/          - Refresh access token
- POST   /api/auth/register/         - Register new user
- POST   /api/auth/logout/           - Logout (blacklist token)
- POST   /api/auth/change-password/  - Change password
- GET    /api/auth/verify/           - Verify token validity

Users:
- GET    /api/users/                 - List users (admin only)
- POST   /api/users/                 - Create user (public)
- GET    /api/users/{id}/            - Get user detail
- PUT    /api/users/{id}/            - Update user
- DELETE /api/users/{id}/            - Delete user
- GET    /api/users/me/              - Get current user

Admins:
- GET    /api/admins/                - List admins
- POST   /api/admins/                - Create admin
- GET    /api/admins/{id}/           - Get admin detail
- PUT    /api/admins/{id}/           - Update admin
- DELETE /api/admins/{id}/           - Delete admin

Auth Users:
- GET    /api/auth-users/            - List auth users
- POST   /api/auth-users/            - Create auth user
- GET    /api/auth-users/{id}/       - Get auth user detail
- PUT    /api/auth-users/{id}/       - Update auth user
- DELETE /api/auth-users/{id}/       - Delete auth user
- POST   /api/auth-users/{id}/grant-station/  - Grant station access
- DELETE /api/auth-users/{id}/revoke-station/{station_id}/  - Revoke station access

Institutions:
- GET    /api/institutions/          - List institutions
- POST   /api/institutions/          - Create institution (admin only)
- GET    /api/institutions/{id}/     - Get institution detail
- PUT    /api/institutions/{id}/     - Update institution
- DELETE /api/institutions/{id}/     - Delete institution

Stations:
- GET    /api/stations/              - List stations
- POST   /api/stations/              - Create station
- GET    /api/stations/{id}/         - Get station detail
- PUT    /api/stations/{id}/         - Update station
- DELETE /api/stations/{id}/         - Delete station
- GET    /api/stations/{id}/alerts/  - Get all alerts for station
- POST   /api/stations/{id}/grant-access/  - Grant access to auth_user
- GET    /api/stations/nearby/?lat=X&lon=Y&radius=Z  - Find nearby stations

Devices:
- GET    /api/devices/               - List devices
- POST   /api/devices/               - Create device
- GET    /api/devices/{id}/          - Get device detail
- PUT    /api/devices/{id}/          - Update device
- DELETE /api/devices/{id}/          - Delete device

Alerts:
- GET    /api/alerts/                - List alerts
- POST   /api/alerts/                - Create alert
- GET    /api/alerts/{id}/           - Get alert detail
- PUT    /api/alerts/{id}/           - Update alert
- DELETE /api/alerts/{id}/           - Delete alert
- POST   /api/alerts/{id}/pollutants/  - Add pollutants to alert ⭐
- POST   /api/alerts/{id}/mark-attended/  - Mark alert as attended
- POST   /api/alerts/{id}/notify/    - Record who received alert

Alert Pollutants:
- GET    /api/alert-pollutants/      - List all pollutants
- POST   /api/alert-pollutants/      - Create pollutant
- GET    /api/alert-pollutants/{id}/ - Get pollutant detail
- PUT    /api/alert-pollutants/{id}/ - Update pollutant
- DELETE /api/alert-pollutants/{id}/ - Delete pollutant

Alert Receives (M2M):
- GET    /api/alert-receives/        - List who received which alerts
- POST   /api/alert-receives/        - Record alert receipt
- DELETE /api/alert-receives/{id}/   - Remove receipt record

Station Consults (M2M):
- GET    /api/station-consults/      - List access permissions
- POST   /api/station-consults/      - Grant access
- DELETE /api/station-consults/{id}/ - Revoke access

Filtering & Pagination:
All list endpoints support:
- ?page=N                 - Page number
- ?page_size=N            - Items per page (max 100)
- ?search=term            - Search in relevant fields
- ?ordering=field         - Sort by field (use -field for descending)
- Custom filters per endpoint (see filters.py)

Examples:
- GET /api/stations/?status=active&institution=5
- GET /api/alerts/?station=10&attended=false&date_after=2024-01-01
- GET /api/devices/?station=3&type=SENSOR
"""