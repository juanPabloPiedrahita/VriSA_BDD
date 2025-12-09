from django.contrib.gis.db import models as geomodels
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    """Manager for User model"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

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

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email instead of username.
    Compatible with Django's authentication system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    password_hash = models.TextField(db_column='password_hash')  # Map to password field
    role = models.CharField(max_length=50, default='citizen')
    
    # Django auth required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'api_user'
    
    def __str__(self):
        return f"{self.name} <{self.email}>"
    
    @property
    def password(self):
        """Map password to password_hash for Django auth"""
        return self.password_hash
    
    @password.setter
    def password(self, value):
        """Map password setter to password_hash"""
        self.password_hash = value
    
    def set_password(self, raw_password):
        """Set password using Django's hash function"""
        from django.contrib.auth.hashers import make_password
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check password using Django's check function"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)


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
