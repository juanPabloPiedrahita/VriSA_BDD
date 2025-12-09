# Migración manual actualizada para soportar AUTH_USER_MODEL
from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.db.models.deletion

SQL_CREATE_EXTENSIONS = """
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""

SQL_CREATE_ENUMS = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'pollutant_type') THEN
        CREATE TYPE pollutant_type AS ENUM ('PM25','PM10','NO2','O3','SO2','CO');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'device_type') THEN
        CREATE TYPE device_type AS ENUM ('SENSOR','METEO','OTHER');
    END IF;
END$$;
"""

SQL_CREATE_ALERT_RECEIVES = """
CREATE TABLE IF NOT EXISTS alert_receives (
    auth_user_id integer NOT NULL REFERENCES api_authuser(id) ON DELETE CASCADE,
    alert_id integer NOT NULL REFERENCES api_alert(id) ON DELETE CASCADE,
    received_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (auth_user_id, alert_id)
);
"""

SQL_CREATE_STATION_CONSULTS = """
CREATE TABLE IF NOT EXISTS station_consults (
    auth_user_id integer NOT NULL REFERENCES api_authuser(id) ON DELETE CASCADE,
    station_id integer NOT NULL REFERENCES api_station(id) ON DELETE CASCADE,
    granted_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (auth_user_id, station_id)
);
"""

SQL_TRIGGER_UPDATED_AT = """
CREATE OR REPLACE FUNCTION trg_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

SQL_CREATE_TRIGGER_ON_STATIONS = """
DROP TRIGGER IF EXISTS trg_stations_updated_at ON api_station;
CREATE TRIGGER trg_stations_updated_at
BEFORE UPDATE ON api_station
FOR EACH ROW
EXECUTE FUNCTION trg_set_updated_at();
"""

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # ← IMPORTANTE: Dependencia de auth
    ]

    operations = [
        migrations.RunSQL(SQL_CREATE_EXTENSIONS),
        migrations.RunSQL(SQL_CREATE_ENUMS),

        # User - Now compatible with Django Auth
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password', db_column='password_hash')),  # ← Agregado
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),  # ← Agregado
                ('is_superuser', models.BooleanField(default=False)),  # ← Agregado
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('role', models.CharField(default='citizen', max_length=50)),
                ('is_active', models.BooleanField(default=True)),  # ← Agregado
                ('is_staff', models.BooleanField(default=False)),  # ← Agregado
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'api_user',
                'abstract': False,
            },
            managers=[
                ('objects', models.Manager()),
            ],
        ),

        # Admins
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('access_level', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, 
                                              to='api.user', 
                                              related_name='admin_profile')),
            ],
        ),

        # AuthUsers
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('read_access', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, 
                                              to='api.user',
                                              related_name='auth_profile')),
            ],
        ),

        # Institutions
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, 
                                           to='api.admin',
                                           related_name='institutions')),
            ],
        ),

        # Station
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('installed_at', models.DateField(null=True, blank=True)),
                ('status', models.CharField(default='inactive', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, 
                                           to='api.admin', 
                                           null=True, 
                                           blank=True,
                                           related_name='stations')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, 
                                                 to='api.institution',
                                                 related_name='stations')),
            ],
        ),

        # Devices
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serial_number', models.CharField(max_length=100)),
                ('install_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, 
                                             to='api.station',
                                             related_name='devices')),
            ],
        ),

        # Alerts
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_date', models.DateTimeField(auto_now_add=True)),
                ('attended', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, 
                                             to='api.station',
                                             related_name='alerts')),
            ],
        ),

        # AlertPollutant
        migrations.CreateModel(
            name='AlertPollutant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pollutant', models.CharField(max_length=10)),
                ('level', models.FloatField()),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, 
                                           to='api.alert',
                                           related_name='pollutants')),
            ],
        ),

        # Many-to-many tables with composite PKs
        migrations.RunSQL(SQL_CREATE_ALERT_RECEIVES),
        migrations.RunSQL(SQL_CREATE_STATION_CONSULTS),

        # Trigger for updated_at
        migrations.RunSQL(SQL_TRIGGER_UPDATED_AT),
        migrations.RunSQL(SQL_CREATE_TRIGGER_ON_STATIONS),

        # Indices
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_users_email ON api_user(email);"),
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_stations_institution ON api_station(institution_id);"),
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_devices_station ON api_device(station_id);"),
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_alerts_station ON api_alert(station_id);"),
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_alert_pollutants_alert ON api_alertpollutant(alert_id);"),
        migrations.RunSQL("CREATE INDEX IF NOT EXISTS idx_alert_pollutants_type ON api_alertpollutant(pollutant);"),
    ]
