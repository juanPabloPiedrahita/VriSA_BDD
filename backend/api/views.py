"""
Views and API ViewSets for VRISA.

This module contains:
- lightweight test endpoints (Redis test, health check)
- DRF viewsets for Users, Admins, AuthUsers, Institutions, Stations, Devices, Alerts,
  AlertPollutants, AlertReceives, and StationConsults
- Custom actions for grant/revoke access, station nearby queries, alert management, etc.

All viewsets use pagination, filtering and permissions defined in other modules.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

def test_redis(request):
    """
    Quick Redis connectivity endpoint.

    This endpoint writes a temporary key into the configured cache (Redis) and
    reads it back immediately to confirm the cache backend works.

    Returns
    -------
    JsonResponse
        JSON object with the retrieved value from Redis under key 'redis_test'.

    Example
    -------
    GET /test-redis/
    Response: {"redis_test": "Hello Redis!"}
    """
    cache.set('test_key', 'Hello Redis!', 30)
    value = cache.get('test_key')
    return JsonResponse({'redis_test': value})


# Apartir de aqui se desarrolla un Endpoint temporal para probar sistema entero, ocho con esto es solo un health check
from django.db import connection
from .models import User

def health_check(request):
    """
    Comprehensive system health-check endpoint.

    Checks performed:
    - Django request handling (if this view executes it's considered ok)
    - PostgreSQL connection (simple SELECT 1)
    - PostGIS extension availability (SELECT PostGIS_version())
    - Redis cache operations (set/get a temporary key)

    Returns
    -------
    JsonResponse
        A dictionary describing the status of each subsystem. Possible values:
        - 'ok' (operational)
        - string with exception message (if error)
        - PostGIS version string (if available)
    """
    result = {
        'django': 'ok',
        'database': None,
        'redis': None,
        'postgis': None,
    }

    # Test PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result['database'] = 'ok'
    except Exception as e:
        result['database'] = str(e)

    # Test PostGIS
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_version()")
            result['postgis'] = cursor.fetchone()[0]
    except Exception as e:
        result['postgis'] = str(e)

    # Test Redis
    try:
        cache.set('health', 'ok', 10)
        if cache.get('health') == 'ok':
            result['redis'] = 'ok'
    except Exception as e:
        result['redis'] = str(e)

    return JsonResponse(result)


# -------------------------
# DRF ViewSets & helpers
# -------------------------
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.db import models

from .models import (
    User, Admin, AuthUser, Institution, Station, Device,
    Alert, AlertPollutant, AlertReceive, StationConsult
)
from .serializers import (
    UserSerializer, UserDetailSerializer,
    AdminSerializer, AdminCreateSerializer,
    AuthUserSerializer, AuthUserCreateSerializer,
    InstitutionSerializer, InstitutionDetailSerializer,
    StationSerializer, StationListSerializer, StationCreateSerializer, StationDetailSerializer,
    DeviceSerializer,
    AlertSerializer, AlertDetailSerializer,
    AlertPollutantSerializer, AlertPollutantCreateSerializer,
    AlertReceiveSerializer,
    StationConsultSerializer,
)
from .permissions import (
    IsAdmin, IsAuthUser, IsAdminOrAuthUser, IsAdminOrReadOnly,
    IsInstitutionAdmin, IsStationAdmin, CanAccessStation, IsOwnerOrAdmin
)
from .pagination import StandardResultsSetPagination
from .filters import StationFilter, AlertFilter, DeviceFilter


# ==================== USER VIEWSETS ====================

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.

    Responsibilities
    ----------------
    - List/Retrieve: available to Admins only
    - Create: public registration endpoint
    - Update/Delete: allowed for the owner or Admins
    - me: returns current authenticated user profile

    Behavior
    --------
    - Uses StandardResultsSetPagination
    - Supports search and ordering via DRF filters
    - Searchable fields: name, email, role
    - Ordering fields: created_at, name, email
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'role']
    ordering_fields = ['created_at', 'name', 'email']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Return appropriate permission classes based on action.

        - create: AllowAny
        - me: IsAuthenticated
        - update/partial_update/destroy: IsAuthenticated + IsOwnerOrAdmin
        - others: IsAuthenticated + IsAdmin
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'me':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_class(self):
        """Return UserDetailSerializer for detailed views, otherwise UserSerializer."""
        if self.action == 'retrieve' or self.action == 'me':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retrieve current authenticated user's profile.

        Returns
        -------
        Response
            Serialized user detail (UserDetailSerializer)
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


# ==================== ADMIN VIEWSETS ====================

class AdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage Admin profiles.

    Notes
    -----
    - Only system admins (users with admin_profile) can manage Admin entities.
    - Uses AdminCreateSerializer when creating nested users + admin in one call.
    - Supports search on user's name and email.
    """
    queryset = Admin.objects.select_related('user').all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__name', 'user__email']
    ordering_fields = ['created_at', 'access_level']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return AdminCreateSerializer for create action, otherwise AdminSerializer."""
        if self.action == 'create':
            return AdminCreateSerializer
        return AdminSerializer


# ==================== AUTH USER VIEWSETS ====================

class AuthUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for authorized (AuthUser) profiles.

    Responsibilities
    ----------------
    - Admins can create, update, delete AuthUser entries.
    - Exposes custom actions:
      - grant-station: assign station access to auth_user
      - revoke-station: remove station access
    """
    queryset = AuthUser.objects.select_related('user').all()
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__name', 'user__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use AuthUserCreateSerializer for creation to accept nested user data."""
        if self.action == 'create':
            return AuthUserCreateSerializer
        return AuthUserSerializer

    @action(detail=True, methods=['post'], url_path='grant-station')
    def grant_station(self, request, pk=None):
        """
        Grant station access to this AuthUser.

        Body
        ----
        {
            "station_id": <int>
        }

        Responses
        ---------
        - 201: access created
        - 200: access already existed
        - 400: missing station_id
        - 404: station not found
        """
        auth_user = self.get_object()
        station_id = request.data.get('station_id')

        if not station_id:
            return Response(
                {'error': 'station_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            station = Station.objects.get(id=station_id)
        except Station.DoesNotExist:
            return Response(
                {'error': 'Station not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        consult, created = StationConsult.objects.get_or_create(
            auth_user=auth_user,
            station=station
        )

        return Response({
            'message': 'Access granted' if created else 'Access already exists',
            'auth_user': auth_user.id,
            'station': station.id,
            'granted_at': consult.granted_at
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='revoke-station/(?P<station_id>[^/.]+)')
    def revoke_station(self, request, pk=None, station_id=None):
        """
        Revoke previously granted station access.

        Path args
        ---------
        station_id : int

        Responses
        ---------
        - 204: access revoked
        - 404: access not found
        """
        auth_user = self.get_object()

        try:
            consult = StationConsult.objects.get(
                auth_user=auth_user,
                station_id=station_id
            )
            consult.delete()
            return Response({'message': 'Access revoked'}, status=status.HTTP_204_NO_CONTENT)
        except StationConsult.DoesNotExist:
            return Response(
                {'error': 'Access not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ==================== INSTITUTION VIEWSETS ====================

class InstitutionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Institution entities.

    Permissions
    -----------
    - Read: any authenticated user
    - Write: admins only (IsAdminOrReadOnly)

    Behavior
    --------
    - Uses InstitutionDetailSerializer for detailed retrieve operations.
    - Supports filtering by verified and admin.
    """
    queryset = Institution.objects.select_related('admin__user').all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    ordering_fields = ['created_at', 'name', 'verified']
    ordering = ['-created_at']
    filterset_fields = ['verified', 'admin']

    def get_serializer_class(self):
        """Return InstitutionDetailSerializer for retrieve, otherwise InstitutionSerializer."""
        if self.action == 'retrieve':
            return InstitutionDetailSerializer
        return InstitutionSerializer


# ==================== STATION VIEWSETS ====================

class StationViewSet(viewsets.ModelViewSet):
    """
    Station management ViewSet with spatial capabilities.

    Responsibilities
    ----------------
    - List/Retrieve: allowed for any authenticated user (read-only for non-admins)
    - Create/Update: admins only
    - Delete: restricted to institution admin (permissions enforced elsewhere)

    Custom actions
    --------------
    - alerts (detail=True, GET): list alerts for a station
    - grant_access (detail=True, POST): grant station access to an auth_user
    - nearby (detail=False, GET): find nearby stations given lat/lon and radius
    """
    queryset = Station.objects.select_related('institution', 'admin__user').prefetch_related('devices')
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = StationFilter
    search_fields = ['name', 'address', 'institution__name']
    ordering_fields = ['created_at', 'name', 'installed_at', 'status']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Return permission classes based on action.

        - list/retrieve/alerts/nearby: IsAuthenticated
        - write operations: IsAuthenticated + IsAdmin
        """
        if self.action in ['list', 'retrieve', 'alerts', 'nearby']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_class(self):
        """
        Choose serializer depending on the action:
        - create/update/partial_update: StationCreateSerializer
        - retrieve: StationDetailSerializer
        - list: StationListSerializer
        - default: StationSerializer
        """
        if self.action in ['create', 'update', 'partial_update']:
            return StationCreateSerializer
        elif self.action == 'retrieve':
            return StationDetailSerializer
        elif self.action == 'list':
            return StationListSerializer
        return StationSerializer

    def get_queryset(self):
        """All authenticated users can see all stations (further filtering done by filters)."""
        return super().get_queryset()

    @action(detail=True, methods=['get'], url_path='alerts')
    def alerts(self, request, pk=None):
        """
        List all alerts associated with the station.

        Query params
        ------------
        - attended: optional boolean 'true' or 'false' to filter attended status

        Pagination
        ----------
        Uses the viewset's paginator if the result set is large.
        """
        station = self.get_object()
        alerts = station.alerts.prefetch_related('pollutants').order_by('-alert_date')

        # Apply filters
        attended = request.query_params.get('attended')
        if attended is not None:
            alerts = alerts.filter(attended=attended.lower() == 'true')

        # Pagination
        page = self.paginate_queryset(alerts)
        if page is not None:
            serializer = AlertSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def grant_access(self, request, pk=None):
        """
        Grant an auth_user access to this station.

        Body
        ----
        {
            "auth_user_id": <int>
        }

        Responses
        ---------
        - 201 created if new
        - 200 ok if already existed
        - 400/404 for errors
        """
        station = self.get_object()
        auth_user_id = request.data.get('auth_user_id')

        if not auth_user_id:
            return Response(
                {'error': 'auth_user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            auth_user = AuthUser.objects.get(id=auth_user_id)
        except AuthUser.DoesNotExist:
            return Response(
                {'error': 'AuthUser not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        consult, created = StationConsult.objects.get_or_create(
            auth_user=auth_user,
            station=station
        )

        serializer = StationConsultSerializer(consult)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Spatial query: find stations within a radius from a point.

        Query params
        ------------
        - lat (required): latitude
        - lon (required): longitude
        - radius (optional): radius in meters (default 5000)

        Returns
        -------
        Response: serialized StationListSerializer objects ordered by distance
        """
        from django.contrib.gis.geos import Point
        from django.contrib.gis.measure import D

        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = request.query_params.get('radius', 5000)  # default 5km

        if not lat or not lon:
            return Response(
                {'error': 'lat and lon parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)
            point = Point(lon, lat, srid=4326)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid coordinates or radius'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stations = self.get_queryset().filter(
            location__distance_lte=(point, D(m=radius))
        ).annotate(
            distance=models.functions.Distance('location', point)
        ).order_by('distance')

        serializer = StationListSerializer(stations, many=True)
        return Response(serializer.data)


# ==================== DEVICE VIEWSETS ====================

class DeviceViewSet(viewsets.ModelViewSet):
    """
    Device management ViewSet.

    Permissions
    -----------
    - list/retrieve: any authenticated user
    - create/update/delete: admins only

    Supports filtering by station and type, searching by serial_number and description.
    """
    queryset = Device.objects.select_related('station').all()
    serializer_class = DeviceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = DeviceFilter
    search_fields = ['serial_number', 'description']
    ordering_fields = ['created_at', 'install_date', 'type']
    ordering = ['-created_at']

    def get_permissions(self):
        """Allow read-only to authenticated users, write operations to admins."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]


# ==================== ALERT VIEWSETS ====================

class AlertViewSet(viewsets.ModelViewSet):
    """
    Alert management ViewSet.

    Responsibilities
    ----------------
    - List/Retrieve: any authenticated user
    - Create/Modify/Delete: admins only (per get_permissions)
    - Custom actions:
      - pollutants: add pollutant records to the alert
      - mark_attended: set alert.attended = True
      - notify: record auth_users that received the alert
    """
    queryset = Alert.objects.select_related('station').prefetch_related('pollutants').all()
    serializer_class = AlertSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = AlertFilter
    search_fields = ['station__name']
    ordering_fields = ['alert_date', 'attended', 'created_at']
    ordering = ['-alert_date']

    def get_permissions(self):
        """List/retrieve allowed to authenticated users; other actions require admin privileges."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_class(self):
        """Use AlertDetailSerializer for retrieve, otherwise AlertSerializer."""
        if self.action == 'retrieve':
            return AlertDetailSerializer
        return AlertSerializer

    @action(detail=True, methods=['post'], url_path='pollutants')
    def add_pollutants(self, request, pk=None):
        """
        Add pollutant records to an existing alert.

        Body
        ----
        {
            "pollutants": [
                {"pollutant": "PM25", "level": 12.3},
                ...
            ]
        }

        Responses
        ---------
        - 201: created pollutants
        - 400: invalid payload / validation errors
        """
        alert = self.get_object()

        # Expect list of pollutants
        pollutants_data = request.data.get('pollutants', [])
        if not isinstance(pollutants_data, list):
            pollutants_data = [pollutants_data]

        created_pollutants = []
        for pollutant_data in pollutants_data:
            pollutant_data['alert'] = alert.id
            serializer = AlertPollutantCreateSerializer(data=pollutant_data)
            if serializer.is_valid():
                pollutant = AlertPollutant.objects.create(
                    alert=alert,
                    **serializer.validated_data
                )
                created_pollutants.append(pollutant)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = AlertPollutantSerializer(created_pollutants, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_attended(self, request, pk=None):
        """
        Mark this alert as attended and return its serialized representation.
        """
        alert = self.get_object()
        alert.attended = True
        alert.save()

        serializer = self.get_serializer(alert)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='notify')
    def notify_users(self, request, pk=None):
        """
        Record that a list of auth_user ids received the alert.

        Body
        ----
        {
            "auth_user_ids": [1, 2, 3]
        }

        Returns
        -------
        Response with message and created receives.
        """
        alert = self.get_object()
        auth_user_ids = request.data.get('auth_user_ids', [])

        if not isinstance(auth_user_ids, list):
            auth_user_ids = [auth_user_ids]

        created = []
        for auth_user_id in auth_user_ids:
            try:
                auth_user = AuthUser.objects.get(id=auth_user_id)
                receive, was_created = AlertReceive.objects.get_or_create(
                    auth_user=auth_user,
                    alert=alert
                )
                if was_created:
                    created.append(receive)
            except AuthUser.DoesNotExist:
                continue

        serializer = AlertReceiveSerializer(created, many=True)
        return Response({
            'message': f'{len(created)} users notified',
            'receives': serializer.data
        }, status=status.HTTP_201_CREATED)


# ==================== ALERT POLLUTANT VIEWSETS ====================

class AlertPollutantViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage AlertPollutant entries.

    Permissions
    -----------
    - Authenticated users with either Admin or AuthUser profiles can access.
    - Typically pollutants are added via Alert.add_pollutants action.
    """
    queryset = AlertPollutant.objects.select_related('alert__station').all()
    serializer_class = AlertPollutantSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAuthUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['pollutant', 'alert']
    ordering_fields = ['recorded_at', 'level']
    ordering = ['-recorded_at']


# ==================== MANY-TO-MANY VIEWSETS ====================

class AlertReceiveViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the AlertReceive join table.

    Only Admins can manage these records via the API.
    """
    queryset = AlertReceive.objects.select_related('auth_user__user', 'alert__station').all()
    serializer_class = AlertReceiveSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['auth_user', 'alert']
    ordering = ['-received_at']


class StationConsultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StationConsult (which auth_user has access to which station).

    Only Admins can manage these records through the API.
    """
    queryset = StationConsult.objects.select_related('auth_user__user', 'station').all()
    serializer_class = StationConsultSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['auth_user', 'station']
    ordering = ['-granted_at']
