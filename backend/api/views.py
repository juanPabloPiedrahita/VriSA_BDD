from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.cache import cache

def test_redis(request):
    cache.set('test_key', 'Hello Redis!', 30)
    value = cache.get('test_key')
    return JsonResponse({'redis_test': value})

#Apartir de aqui se desarrolla un Endpoint temporal para probar sistema entero, ocho con esto es solo un health check
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from .models import User

def health_check(request):
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

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

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
    ViewSet for users.
    - List/Retrieve: Admins only
    - Create: Public (registration)
    - Update/Delete: Owner or Admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'role']
    ordering_fields = ['created_at', 'name', 'email']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated(), IsAdmin()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


# ==================== ADMIN VIEWSETS ====================

class AdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet for admins.
    Only system admins can manage other admins.
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
        if self.action == 'create':
            return AdminCreateSerializer
        return AdminSerializer


# ==================== AUTH USER VIEWSETS ====================

class AuthUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for authorized users.
    Admins can manage auth_users.
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
        if self.action == 'create':
            return AuthUserCreateSerializer
        return AuthUserSerializer
    
    @action(detail=True, methods=['post'], url_path='grant-station')
    def grant_station(self, request, pk=None):
        """Grant access to a station for this auth_user"""
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
        """Revoke access to a station for this auth_user"""
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
    ViewSet for institutions.
    - List/Retrieve: All authenticated users
    - Create/Update/Delete: Admins only
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
        if self.action == 'retrieve':
            return InstitutionDetailSerializer
        return InstitutionSerializer


# ==================== STATION VIEWSETS ====================

class StationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for stations with spatial queries support.
    - List/Retrieve: Auth users with access
    - Create/Update: Station or Institution admins
    - Delete: Institution admin only
    
    Custom actions:
    - alerts: Get all alerts for a station
    - grant_access: Grant access to an auth_user
    - nearby: Find stations within radius
    """
    queryset = Station.objects.select_related('institution', 'admin__user').prefetch_related('devices')
    permission_classes = [IsAuthenticated, IsAdminOrAuthUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = StationFilter
    search_fields = ['name', 'address', 'institution__name']
    ordering_fields = ['created_at', 'name', 'installed_at', 'status']
    ordering = ['-created_at']

    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return StationCreateSerializer
        elif self.action == 'retrieve':
            return StationDetailSerializer
        elif self.action == 'list':
            return StationListSerializer
        return StationSerializer
    
    def get_queryset(self):
        """Filter stations based on user permissions"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Admins see all stations
        if hasattr(user, 'admin_profile'):
            return queryset
        
        # Auth users see only stations they have access to
        if hasattr(user, 'auth_profile'):
            return queryset.filter(
                consults__auth_user=user.auth_profile
            ).distinct()
        
        return queryset.none()
    
    @action(detail=True, methods=['get'], url_path='alerts')
    def alerts(self, request, pk=None):
        """Get all alerts for this station"""
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
        """Grant access to this station for an auth_user"""
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
        """Find stations within a radius (in meters) from a point"""
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
    ViewSet for devices.
    - List/Retrieve: Users with access to the station
    - Create/Update/Delete: Station admin
    """
    queryset = Device.objects.select_related('station').all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAuthUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = DeviceFilter
    search_fields = ['serial_number', 'description']
    ordering_fields = ['created_at', 'install_date', 'type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter devices based on station access"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Admins see all
        if hasattr(user, 'admin_profile'):
            return queryset
        
        # Auth users see devices from accessible stations
        if hasattr(user, 'auth_profile'):
            accessible_stations = Station.objects.filter(
                consults__auth_user=user.auth_profile
            )
            return queryset.filter(station__in=accessible_stations)
        
        return queryset.none()


# ==================== ALERT VIEWSETS ====================

class AlertViewSet(viewsets.ModelViewSet):
    """
    ViewSet for alerts.
    
    Custom actions:
    - add_pollutants: POST /alerts/{id}/pollutants/
    - mark_attended: Mark alert as attended
    - notify_users: Record who received the alert
    """
    queryset = Alert.objects.select_related('station').prefetch_related('pollutants').all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAuthUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = AlertFilter
    search_fields = ['station__name']
    ordering_fields = ['alert_date', 'attended', 'created_at']
    ordering = ['-alert_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlertDetailSerializer
        return AlertSerializer
    
    def get_queryset(self):
        """Filter alerts based on station access"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Admins see all
        if hasattr(user, 'admin_profile'):
            return queryset
        
        # Auth users see alerts from accessible stations
        if hasattr(user, 'auth_profile'):
            accessible_stations = Station.objects.filter(
                consults__auth_user=user.auth_profile
            )
            return queryset.filter(station__in=accessible_stations)
        
        return queryset.none()
    
    @action(detail=True, methods=['post'], url_path='pollutants')
    def add_pollutants(self, request, pk=None):
        """Add pollutants to an alert: POST /alerts/{id}/pollutants/"""
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
        """Mark alert as attended"""
        alert = self.get_object()
        alert.attended = True
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='notify')
    def notify_users(self, request, pk=None):
        """Record that auth_users received this alert"""
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

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        station = self.get_object()
        return Response({
            'total_alerts': station.alerts.count(),
            'alerts_attended': station.alerts.filter(attended=True).count(),
            'total_devices': station.devices.count(),
            'active_devices': station.devices.filter(type='SENSOR').count(),
        })

# ==================== ALERT POLLUTANT VIEWSETS ====================

class AlertPollutantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for alert pollutants.
    Usually accessed via Alert.add_pollutants action.
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
    ViewSet for alert receives (who received which alert).
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
    ViewSet for station consults (who has access to which station).
    """
    queryset = StationConsult.objects.select_related('auth_user__user', 'station').all()
    serializer_class = StationConsultSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['auth_user', 'station']
    ordering = ['-granted_at']