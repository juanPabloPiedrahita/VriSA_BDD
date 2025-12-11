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
    """
    Serializer for the User model.

    Handles password hashing on create/update and hides password fields
    from API responses. Used for basic user CRUD operations.
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Hash the password before creating the user.
        """
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Hash the password when updating the user (if provided).
        """
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(UserSerializer):
    """
    Extends UserSerializer to include role flags (admin or auth_user).
    """
    is_admin = serializers.SerializerMethodField()
    is_auth_user = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['is_admin', 'is_auth_user']

    def get_is_admin(self, obj):
        """Returns True if the user has an admin profile."""
        return hasattr(obj, 'admin_profile')

    def get_is_auth_user(self, obj):
        """Returns True if the user has an auth_user profile."""
        return hasattr(obj, 'auth_profile')


# ==================== ADMIN SERIALIZERS ====================

class AdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the Admin model.
    Includes nested read-only user info and a write-only user_id.
    """
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
    """
    Serializer for creating an Admin along with its associated User.
    Includes full embedded user data.
    """
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['id', 'access_level', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create both User and Admin in a single request."""
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin


# ==================== AUTH USER SERIALIZERS ====================

class AuthUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the AuthUser model.
    Includes nested read-only user data and a write-only user_id.
    """
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
    """
    Serializer for creating an AuthUser with embedded user data.
    """
    user = UserSerializer()

    class Meta:
        model = AuthUser
        fields = ['id', 'read_access', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create both User and AuthUser."""
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        auth_user = AuthUser.objects.create(user=user, **validated_data)
        return auth_user


# ==================== INSTITUTION SERIALIZERS ====================

class InstitutionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Institution model.
    Includes admin name and station count as computed fields.
    """
    admin_name = serializers.CharField(source='admin.user.name', read_only=True)
    stations_count = serializers.SerializerMethodField()

    class Meta:
        model = Institution
        fields = ['id', 'name', 'address', 'verified', 'admin', 'admin_name',
                  'stations_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_stations_count(self, obj):
        """Return the number of stations owned by the institution."""
        return obj.stations.count()


class InstitutionDetailSerializer(InstitutionSerializer):
    """
    Detailed serializer for Institution.
    Includes full list of stations.
    """
    stations = serializers.SerializerMethodField()

    class Meta(InstitutionSerializer.Meta):
        fields = InstitutionSerializer.Meta.fields + ['stations']

    def get_stations(self, obj):
        """Return serialized stations belonging to this institution."""
        from .serializers import StationListSerializer
        return StationListSerializer(obj.stations.all(), many=True).data


# ==================== DEVICE SERIALIZERS ====================

class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Device model.
    Includes station name (read-only).
    """
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'install_date', 'description',
                  'type', 'station', 'station_name', 'created_at']
        read_only_fields = ['id', 'install_date', 'created_at']


# ==================== ALERT POLLUTANT SERIALIZERS ====================

class AlertPollutantSerializer(serializers.ModelSerializer):
    """
    Serializer for pollutant measurements associated with an alert.
    """
    class Meta:
        model = AlertPollutant
        fields = ['id', 'alert', 'pollutant', 'level', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class AlertPollutantCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding pollutant info when creating an alert.
    """
    class Meta:
        model = AlertPollutant
        fields = ['pollutant', 'level']


# ==================== ALERT SERIALIZERS ====================

class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alert model.
    Includes pollutants and station name.
    """
    pollutants = AlertPollutantSerializer(many=True, read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Alert
        fields = ['id', 'alert_date', 'attended', 'station', 'station_name',
                  'pollutants', 'created_at']
        read_only_fields = ['id', 'alert_date', 'created_at']


class AlertDetailSerializer(AlertSerializer):
    """
    Detailed alert serializer including users who received the alert.
    """
    receivers = serializers.SerializerMethodField()

    class Meta(AlertSerializer.Meta):
        fields = AlertSerializer.Meta.fields + ['receivers']

    def get_receivers(self, obj):
        """Return user names and timestamps for alert receivers."""
        receives = AlertReceive.objects.filter(alert=obj).select_related('auth_user__user')
        return [{
            'auth_user_id': r.auth_user.id,
            'user_name': r.auth_user.user.name,
            'user_email': r.auth_user.user.email,
            'received_at': r.received_at
        } for r in receives]


# ==================== STATION SERIALIZERS ====================

class StationListSerializer(serializers.ModelSerializer):
    """
    Simplified station serializer used for lists.
    Includes institution/admin names and basic location.
    """
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    admin_name = serializers.CharField(source='admin.user.name', read_only=True, allow_null=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ['id', 'name', 'address', 'status', 'institution', 'institution_name',
                  'admin_name', 'location', 'installed_at']

    def get_location(self, obj):
        """Return location as GeoJSON-like dictionary."""
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None


class StationSerializer(GeoFeatureModelSerializer):
    """
    Full serializer for Station with GeoJSON support.
    Includes computed counts for devices and alerts.
    """
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
        """Return number of devices in the station."""
        return obj.devices.count()

    def get_alerts_count(self, obj):
        """Return number of alerts reported by this station."""
        return obj.alerts.count()


class StationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating stations.
    Accepts coordinates as [longitude, latitude] and converts to Point.
    """
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
        """
        Validate and convert [lon, lat] to a GEOS Point.
        """
        try:
            lon, lat = value
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                raise serializers.ValidationError("Invalid coordinates")
            return Point(lon, lat, srid=4326)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Location must be [longitude, latitude]")

    def to_representation(self, instance):
        """
        Convert Point object back into GeoJSON-like format.
        """
        rep = super().to_representation(instance)
        if instance.location:
            rep['location'] = {
                'type': 'Point',
                'coordinates': [instance.location.x, instance.location.y]
            }
        return rep


class StationDetailSerializer(StationSerializer):
    """
    Full detail of a station, including devices and recent alerts.
    """
    devices = DeviceSerializer(many=True, read_only=True)
    recent_alerts = serializers.SerializerMethodField()

    class Meta(StationSerializer.Meta):
        fields = StationSerializer.Meta.fields + ['devices', 'recent_alerts']

    def get_recent_alerts(self, obj):
        """Return the latest 10 alerts sorted by date."""
        alerts = obj.alerts.order_by('-alert_date')[:10]
        return AlertSerializer(alerts, many=True).data


# ==================== MANY-TO-MANY SERIALIZERS ====================

class AlertReceiveSerializer(serializers.ModelSerializer):
    """
    Serializer for AlertReceive relation.
    Provides readable user and alert info.
    """
    auth_user_name = serializers.CharField(source='auth_user.user.name', read_only=True)
    alert_info = serializers.SerializerMethodField()

    class Meta:
        model = AlertReceive
        fields = ['auth_user', 'auth_user_name', 'alert', 'alert_info', 'received_at']
        read_only_fields = ['received_at']

    def get_alert_info(self, obj):
        """Return basic alert metadata."""
        return {
            'id': obj.alert.id,
            'station': obj.alert.station.name,
            'date': obj.alert.alert_date
        }


class StationConsultSerializer(serializers.ModelSerializer):
    """
    Serializer for the StationConsult relationship.
    Indicates which auth_user has access to which station.
    """
    auth_user_name = serializers.CharField(source='auth_user.user.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = StationConsult
        fields = ['auth_user', 'auth_user_name', 'station', 'station_name', 'granted_at']
        read_only_fields = ['granted_at']