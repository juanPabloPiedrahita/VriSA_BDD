from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import make_password
from .models import (
    User, Admin, AuthUser, Institution, Station, Device,
    Alert, AlertPollutant, AlertReceive, StationConsult
)


# ==================== USER SERIALIZERS ====================

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer with password handling"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(UserSerializer):
    """Detailed user with related profiles"""
    is_admin = serializers.SerializerMethodField()
    is_auth_user = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['is_admin', 'is_auth_user']
    
    def get_is_admin(self, obj):
        return hasattr(obj, 'admin_profile')
    
    def get_is_auth_user(self, obj):
        return hasattr(obj, 'auth_profile')


# ==================== ADMIN SERIALIZERS ====================

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Admin
        fields = ['id', 'access_level', 'user', 'user_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class AdminCreateSerializer(serializers.ModelSerializer):
    """Create admin with embedded user data"""
    user = UserSerializer()
    
    class Meta:
        model = Admin
        fields = ['id', 'access_level', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin


# ==================== AUTH USER SERIALIZERS ====================

class AuthUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = AuthUser
        fields = ['id', 'read_access', 'user', 'user_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class AuthUserCreateSerializer(serializers.ModelSerializer):
    """Create auth_user with embedded user data"""
    user = UserSerializer()
    
    class Meta:
        model = AuthUser
        fields = ['id', 'read_access', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        auth_user = AuthUser.objects.create(user=user, **validated_data)
        return auth_user


# ==================== INSTITUTION SERIALIZERS ====================

class InstitutionSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.user.name', read_only=True)
    stations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Institution
        fields = ['id', 'name', 'address', 'verified', 'admin', 'admin_name', 
                  'stations_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_stations_count(self, obj):
        return obj.stations.count()


class InstitutionDetailSerializer(InstitutionSerializer):
    """Detailed institution with all stations"""
    stations = serializers.SerializerMethodField()
    
    class Meta(InstitutionSerializer.Meta):
        fields = InstitutionSerializer.Meta.fields + ['stations']
    
    def get_stations(self, obj):
        from .serializers import StationListSerializer
        return StationListSerializer(obj.stations.all(), many=True).data


# ==================== DEVICE SERIALIZERS ====================

class DeviceSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'install_date', 'description', 
                  'type', 'station', 'station_name', 'created_at']
        read_only_fields = ['id', 'install_date', 'created_at']


# ==================== ALERT POLLUTANT SERIALIZERS ====================

class AlertPollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertPollutant
        fields = ['id', 'alert', 'pollutant', 'level', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class AlertPollutantCreateSerializer(serializers.ModelSerializer):
    """For adding pollutants to an alert"""
    class Meta:
        model = AlertPollutant
        fields = ['pollutant', 'level']


# ==================== ALERT SERIALIZERS ====================

class AlertSerializer(serializers.ModelSerializer):
    pollutants = AlertPollutantSerializer(many=True, read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'alert_date', 'attended', 'station', 'station_name', 
                  'pollutants', 'created_at']
        read_only_fields = ['id', 'alert_date', 'created_at']


class AlertDetailSerializer(AlertSerializer):
    """Detailed alert with receivers"""
    receivers = serializers.SerializerMethodField()
    
    class Meta(AlertSerializer.Meta):
        fields = AlertSerializer.Meta.fields + ['receivers']
    
    def get_receivers(self, obj):
        receives = AlertReceive.objects.filter(alert=obj).select_related('auth_user__user')
        return [{
            'auth_user_id': r.auth_user.id,
            'user_name': r.auth_user.user.name,
            'user_email': r.auth_user.user.email,
            'received_at': r.received_at
        } for r in receives]


# ==================== STATION SERIALIZERS ====================

class StationListSerializer(serializers.ModelSerializer):
    """Simplified station for lists"""
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    admin_name = serializers.CharField(source='admin.user.name', read_only=True, allow_null=True)
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        fields = ['id', 'name', 'address', 'status', 'institution', 'institution_name',
                  'admin_name', 'location', 'installed_at']
    
    def get_location(self, obj):
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None


class StationSerializer(GeoFeatureModelSerializer):
    """Full station with GeoJSON support"""
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    admin_name = serializers.CharField(source='admin.user.name', read_only=True, allow_null=True)
    devices_count = serializers.SerializerMethodField()
    alerts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        geo_field = 'location'
        fields = ['id', 'name', 'description', 'address', 'institution', 'institution_name',
                  'admin', 'admin_name', 'installed_at', 'status', 'devices_count', 
                  'alerts_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_devices_count(self, obj):
        return obj.devices.count()
    
    def get_alerts_count(self, obj):
        return obj.alerts.count()


class StationCreateSerializer(serializers.ModelSerializer):
    """Create/update station with location as [lon, lat]"""
    location = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
        help_text="Location as [longitude, latitude]"
    )
    
    class Meta:
        model = Station
        fields = ['id', 'name', 'description', 'address', 'institution', 'admin',
                  'location', 'installed_at', 'status']
        read_only_fields = ['id']
    
    def validate_location(self, value):
        """Convert [lon, lat] to Point"""
        try:
            lon, lat = value
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                raise serializers.ValidationError("Invalid coordinates")
            return Point(lon, lat, srid=4326)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Location must be [longitude, latitude]")
    
    def to_representation(self, instance):
        """Return location as GeoJSON in response"""
        rep = super().to_representation(instance)
        if instance.location:
            rep['location'] = {
                'type': 'Point',
                'coordinates': [instance.location.x, instance.location.y]
            }
        return rep


class StationDetailSerializer(StationSerializer):
    """Station with all related data"""
    devices = DeviceSerializer(many=True, read_only=True)
    recent_alerts = serializers.SerializerMethodField()
    
    class Meta(StationSerializer.Meta):
        fields = StationSerializer.Meta.fields + ['devices', 'recent_alerts']
    
    def get_recent_alerts(self, obj):
        alerts = obj.alerts.order_by('-alert_date')[:10]
        return AlertSerializer(alerts, many=True).data


# ==================== MANY-TO-MANY SERIALIZERS ====================

class AlertReceiveSerializer(serializers.ModelSerializer):
    auth_user_name = serializers.CharField(source='auth_user.user.name', read_only=True)
    alert_info = serializers.SerializerMethodField()
    
    class Meta:
        model = AlertReceive
        fields = ['auth_user', 'auth_user_name', 'alert', 'alert_info', 'received_at']
        read_only_fields = ['received_at']
    
    def get_alert_info(self, obj):
        return {
            'id': obj.alert.id,
            'station': obj.alert.station.name,
            'date': obj.alert.alert_date
        }


class StationConsultSerializer(serializers.ModelSerializer):
    auth_user_name = serializers.CharField(source='auth_user.user.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = StationConsult
        fields = ['auth_user', 'auth_user_name', 'station', 'station_name', 'granted_at']
        read_only_fields = ['granted_at']