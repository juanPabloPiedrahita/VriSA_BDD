import django_filters
from .models import Station, Alert, Device, AlertPollutant


class StationFilter(django_filters.FilterSet):
    """
    Filters for Station objects.

    Supports:
    - status, institution, admin
    - installed_after, installed_before (date range)
    - name (case-insensitive substring match)
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
    Filters for Alert objects.

    Supports:
    - station, attended
    - date_after, date_before (datetime range)
    - has_pollutant (custom filter by pollutant type)
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
        """
        Filter alerts that contain a specific pollutant type.

        Parameters:
            queryset: Current queryset being filtered.
            name: Name of the filter field.
            value: Pollutant code (e.g., 'PM25').

        Returns:
            Filtered queryset with alerts containing the pollutant.
        """
        return queryset.filter(pollutants__pollutant=value.upper()).distinct()


class DeviceFilter(django_filters.FilterSet):
    """
    Filters for Device objects.

    Supports:
    - station, type
    - installed_after, installed_before (date range)
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
    Filters for AlertPollutant objects.

    Supports:
    - pollutant type
    - level_min / level_max (numeric range)
    - recorded_after / recorded_before (datetime range)
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