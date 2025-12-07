from rest_framework import serializers
from .models import (
    User, Admin, AuthUser, Institution, Station, Device,
    Alert, AlertPollutant, AlertReceive, StationConsult
)
from django.contrib.gis.geos import Point

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at')

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ('id','created_at')

class AuthUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AuthUser
        fields = '__all__'
        read_only_fields = ('id','created_at')

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        read_only_fields = ('id','created_at')

class StationSerializer(serializers.ModelSerializer):
    # location can be passed as [lon, lat] or as GeoJSON; for simplicity accept list
    location = serializers.ListField(child=serializers.FloatField(), min_length=2, max_length=2)

    class Meta:
        model = Station
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at')

    def to_internal_value(self, data):
        # Convert list to Point for the model field
        if 'location' in data and isinstance(data['location'], (list,tuple)):
            lon, lat = data['location']
            data['location'] = Point(lon, lat)
        return super().to_internal_value(data)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('id','created_at')

class AlertPollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertPollutant
        fields = '__all__'
        read_only_fields = ('id','recorded_at')

class AlertSerializer(serializers.ModelSerializer):
    pollutants = AlertPollutantSerializer(many=True, read_only=True)
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ('id','created_at')

class AlertReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertReceive
        fields = '__all__'
        read_only_fields = ()

class StationConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationConsult
        fields = '__all__'
        read_only_fields = ()
