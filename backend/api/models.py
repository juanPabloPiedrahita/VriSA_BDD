from django.contrib.gis.db import models as geomodels
from django.db import models

class PollutantType(models.TextChoices):
    PM25 = 'PM25', 'PM25'
    PM10 = 'PM10', 'PM10'
    NO2  = 'NO2',  'NO2'
    O3   = 'O3',   'O3'
    SO2  = 'SO2',  'SO2'
    CO   = 'CO',   'CO'

class DeviceType(models.TextChoices):
    SENSOR = 'SENSOR', 'SENSOR'
    METEO  = 'METEO',  'METEO'
    OTHER  = 'OTHER',  'OTHER'

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True, db_index=True)
    password_hash = models.TextField()
    role = models.CharField(max_length=50, default='citizen')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Admin(models.Model):
    access_level = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin {self.user.email} (level {self.access_level})"

class AuthUser(models.Model):
    read_access = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuthUser {self.user.email}"

class Institution(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    verified = models.BooleanField(default=False)
    admin = models.ForeignKey(Admin, on_delete=models.RESTRICT, related_name='institutions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Station(models.Model):
    STATUS_CHOICES = (
        ('inactive','inactive'),
        ('active','active'),
        ('maintenance','maintenance'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='stations')
    # DDL intended ON DELETE SET NULL: make this nullable
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='stations')
    location = geomodels.PointField(geography=True, srid=4326)
    installed_at = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=32, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    serial_number = models.CharField(max_length=100)
    install_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=DeviceType.choices)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='devices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} ({self.type})"

class Alert(models.Model):
    alert_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='alerts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.id} @ {self.station.name} - {self.alert_date}"

class AlertPollutant(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='pollutants')
    pollutant = models.CharField(max_length=10, choices=PollutantType.choices)
    level = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pollutant}: {self.level} ({self.alert_id})"

# The two many-to-many join tables in the DDL have composite PKs; Django doesn't support composite PKs natively.
# We'll represent them as models for convenience but also create the real composite-PK tables via migration SQL.
class AlertReceive(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='received_alerts')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='receivers')
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Keep uniqueness constraint; the actual DB PK (composite) will be created in migration SQL.
        unique_together = (('auth_user','alert'),)
        indexes = [
            models.Index(fields=['auth_user','alert']),
        ]

class StationConsult(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='consulted_stations')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='consults')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('auth_user','station'),)
        indexes = [
            models.Index(fields=['auth_user','station']),
        ]
