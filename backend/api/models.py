from django.contrib.gis.db import models as geomodels
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Provides helper methods for creating regular users
    and superusers using email instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a new user with email and optional password.

        Parameters:
            email (str): User's email.
            password (str): Raw password to be hashed.
            extra_fields (dict): Additional fields for the model.

        Raises:
            ValueError: If email is missing.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser with admin privileges.

        Parameters:
            email (str): Superuser email.
            password (str): Password for the account.
            extra_fields (dict): Additional fields.

        Returns:
            User: The created superuser object.
        """
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class PollutantType(models.TextChoices):
    """Enumeration of pollutant types."""
    PM25 = 'PM25', 'PM25'
    PM10 = 'PM10', 'PM10'
    NO2  = 'NO2',  'NO2'
    O3   = 'O3',   'O3'
    SO2  = 'SO2',  'SO2'
    CO   = 'CO',   'CO'


class DeviceType(models.TextChoices):
    """Enumeration of device types."""
    SENSOR = 'SENSOR', 'SENSOR'
    METEO  = 'METEO',  'METEO'
    OTHER  = 'OTHER',  'OTHER'


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for VRISA.

    Uses email as the authentication identifier and stores
    hashed passwords manually in `password_hash`, allowing
    compatibility with Django's auth system.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    password_hash = models.TextField(db_column='password_hash')
    role = models.CharField(max_length=50, default='citizen')

    # Django auth-related fields
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
        """
        Expose password hash for Django compatibility.

        Returns:
            str: The stored password hash.
        """
        return self.password_hash

    @password.setter
    def password(self, value):
        """
        Set password hash directly.

        Parameters:
            value (str): Raw or hashed password.
        """
        self.password_hash = value

    def set_password(self, raw_password):
        """
        Hash and store password using Django's utilities.

        Parameters:
            raw_password (str): Raw user password.
        """
        from django.contrib.auth.hashers import make_password
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Validate raw password against stored hash.

        Parameters:
            raw_password (str): Raw password input.

        Returns:
            bool: True if password matches, otherwise False.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)


class Admin(models.Model):
    """
    Model representing admin users with access levels.
    Linked 1-to-1 with User.
    """

    access_level = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin {self.user.email} (level {self.access_level})"


class AuthUser(models.Model):
    """
    Model for authenticated users with read-only access.
    Linked 1-to-1 with User.
    """

    read_access = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuthUser {self.user.email}"


class Institution(models.Model):
    """
    Model representing an institution that manages stations.
    """

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    verified = models.BooleanField(default=False)
    admin = models.ForeignKey(Admin, on_delete=models.RESTRICT, related_name='institutions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    """
    Represents a monitoring station with geospatial location,
    associated admin, and current status.
    """

    STATUS_CHOICES = (
        ('inactive','inactive'),
        ('active','active'),
        ('maintenance','maintenance'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='stations')
    admin = models.ForeignKey(
        Admin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stations'
    )
    location = geomodels.PointField(geography=True, srid=4326)
    installed_at = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=32, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Represents a device installed in a station.

    Includes sensors and meteorological equipment.
    """

    serial_number = models.CharField(max_length=100)
    install_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=DeviceType.choices)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='devices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} ({self.type})"


class Alert(models.Model):
    """
    Represents a generated alert from a station due to air quality issues.
    """

    alert_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='alerts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.id} @ {self.station.name} - {self.alert_date}"


class AlertPollutant(models.Model):
    """
    Represents pollutant measurements associated with an alert.
    """

    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='pollutants')
    pollutant = models.CharField(max_length=10, choices=PollutantType.choices)
    level = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pollutant}: {self.level} ({self.alert_id})"


class AlertReceive(models.Model):
    """
    Join table representing which authenticated users received a specific alert.

    Django does not support composite primary keys, so uniqueness is enforced
    through constraints instead.
    """

    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='received_alerts')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='receivers')
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('auth_user','alert'),)
        indexes = [
            models.Index(fields=['auth_user','alert']),
        ]


class StationConsult(models.Model):
    """
    Records which stations have been consulted by authenticated users.

    Used to track user interaction history.
    """

    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='consulted_stations')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='consults')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('auth_user','station'),)
        indexes = [
            models.Index(fields=['auth_user','station']),
        ]