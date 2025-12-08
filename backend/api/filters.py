import django_filters
from .models import Station, Alert, Device, AlertPollutant


class StationFilter(django_filters.FilterSet):
    """
    Filters for stations:
    - status, institution, admin
    - installed_after, installed_before (date range)
    - name (case-insensitive contains)
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Station.STATUS_CHOICES)
    institution = django_filters.NumberFilter(field_name='institution__id')
    admin = django_filters.NumberFilter(field_name='admin__id')
    installed_after = django_filters.DateFilter(field_name='installed_at', lookup_expr='gte')
    installed_before = django_filters.DateFilter(field_name='installed_at', lookup_expr='lte')
    
    class Meta:
        model = Station
        fields = ['status', 'institution', 'admin', 'name']


class AlertFilter(django_filters.FilterSet):
    """
    Filters for alerts:
    - station, attended
    - date_after, date_before (datetime range)
    - has_pollutant (filter by pollutant type)
    """
    station = django_filters.NumberFilter(field_name='station__id')
    attended = django_filters.BooleanFilter()
    date_after = django_filters.DateTimeFilter(field_name='alert_date', lookup_expr='gte')
    date_before = django_filters.DateTimeFilter(field_name='alert_date', lookup_expr='lte')
    has_pollutant = django_filters.CharFilter(method='filter_by_pollutant')
    
    class Meta:
        model = Alert
        fields = ['station', 'attended']
    
    def filter_by_pollutant(self, queryset, name, value):
        """Filter alerts that have a specific pollutant"""
        return queryset.filter(pollutants__pollutant=value.upper()).distinct()


class DeviceFilter(django_filters.FilterSet):
    """
    Filters for devices:
    - station, type
    - installed_after, installed_before
    """
    station = django_filters.NumberFilter(field_name='station__id')
    type = django_filters.ChoiceFilter(choices=[
        ('SENSOR', 'SENSOR'),
        ('METEO', 'METEO'),
        ('OTHER', 'OTHER'),
    ])
    installed_after = django_filters.DateTimeFilter(field_name='install_date', lookup_expr='gte')
    installed_before = django_filters.DateTimeFilter(field_name='install_date', lookup_expr='lte')
    
    class Meta:
        model = Device
        fields = ['station', 'type']


class AlertPollutantFilter(django_filters.FilterSet):
    """
    Filters for alert pollutants:
    - pollutant type
    - level range (min/max)
    - date range
    """
    pollutant = django_filters.ChoiceFilter(choices=[
        ('PM25', 'PM25'),
        ('PM10', 'PM10'),
        ('NO2', 'NO2'),
        ('O3', 'O3'),
        ('SO2', 'SO2'),
        ('CO', 'CO'),
    ])
    level_min = django_filters.NumberFilter(field_name='level', lookup_expr='gte')
    level_max = django_filters.NumberFilter(field_name='level', lookup_expr='lte')
    recorded_after = django_filters.DateTimeFilter(field_name='recorded_at', lookup_expr='gte')
    recorded_before = django_filters.DateTimeFilter(field_name='recorded_at', lookup_expr='lte')
    
    class Meta:
        model = AlertPollutant
        fields = ['pollutant', 'alert']