#!/usr/bin/env python
"""
Seed script for populating the VRISA database with test data.

This script creates:
- Users (Admin, Researcher, Citizen)
- Admin profiles
- AuthUsers (authorized users)
- Institutions
- Monitoring stations
- Devices
- Sample alerts with pollutants

Run with:
    docker compose exec backend python seed_data.py

Each function checks for existing records to avoid duplicates.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import (
    User, Admin, AuthUser, Institution, Station,
    Device, Alert, AlertPollutant
)
from django.contrib.gis.geos import Point


def create_users():
    """Create test users: Admin, Researcher, Citizen.

    Returns:
        tuple: (admin_user, researcher_user, citizen_user)
    """
    print("📝 Creating users...")

    # Admin user
    admin_user, created = User.objects.get_or_create(
        email='admin@vrisa.com',
        defaults={
            'name': 'Admin VRISA',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"  ✓ Admin user: {admin_user.email}")

    # Researcher user
    researcher_user, created = User.objects.get_or_create(
        email='researcher@vrisa.com',
        defaults={
            'name': 'Dr. María García',
            'role': 'researcher'
        }
    )
    if created:
        researcher_user.set_password('researcher123')
        researcher_user.save()
        print(f"  ✓ Researcher: {researcher_user.email}")

    # Citizen user
    citizen_user, created = User.objects.get_or_create(
        email='citizen@vrisa.com',
        defaults={
            'name': 'Juan Ciudadano',
            'role': 'citizen'
        }
    )
    if created:
        citizen_user.set_password('citizen123')
        citizen_user.save()
        print(f"  ✓ Citizen: {citizen_user.email}")

    return admin_user, researcher_user, citizen_user


def create_admin_profiles(admin_user):
    """Create admin profile for the given user.

    Args:
        admin_user (User): User instance with role 'admin'

    Returns:
        Admin: Admin profile instance
    """
    print("\n👤 Creating admin profiles...")

    admin, created = Admin.objects.get_or_create(
        user=admin_user,
        defaults={'access_level': 5}
    )
    if created:
        print(f"  ✓ Admin profile created for {admin.user.name}")

    return admin


def create_auth_users(researcher_user):
    """Create AuthUser (authorized user) profile for a researcher.

    Args:
        researcher_user (User): User instance with role 'researcher'

    Returns:
        AuthUser: AuthUser instance
    """
    print("\n🔐 Creating authorized users...")

    auth_user, created = AuthUser.objects.get_or_create(
        user=researcher_user,
        defaults={'read_access': True}
    )
    if created:
        print(f"  ✓ AuthUser created for {auth_user.user.name}")

    return auth_user


def create_institutions(admin):
    """Create sample institutions.

    Args:
        admin (Admin): Admin instance responsible for institutions

    Returns:
        list: List of Institution instances
    """
    print("\n Creating institutions...")

    institutions = []

    inst_data = [
        {
            'name': 'CVC - Corporación Autónoma Regional',
            'address': 'Calle 25 Norte #5N-45, Cali',
            'verified': True
        },
        {
            'name': 'DAGMA - Departamento Administrativo de Gestión del Medio Ambiente',
            'address': 'Carrera 56 #11-36, Cali',
            'verified': True
        },
        {
            'name': 'Universidad del Valle',
            'address': 'Ciudad Universitaria Meléndez, Cali',
            'verified': True
        }
    ]

    for data in inst_data:
        inst, created = Institution.objects.get_or_create(
            name=data['name'],
            defaults={
                'address': data['address'],
                'verified': data['verified'],
                'admin': admin
            }
        )
        if created:
            print(f"  ✓ Institution: {inst.name}")
        institutions.append(inst)

    return institutions


def create_stations(institutions, admin):
    """Create monitoring stations with sample coordinates.

    Args:
        institutions (list): List of Institution instances
        admin (Admin): Admin responsible for stations

    Returns:
        list: List of Station instances
    """
    print("\n Creating stations...")

    stations = []

    station_data = [
        {
            'name': 'Estación Centro',
            'description': 'Estación de monitoreo en el centro de Cali',
            'address': 'Carrera 5 con Calle 12',
            'institution': institutions[0],
            'location': Point(-76.5319, 3.4516, srid=4326),
            'installed_at': '2023-01-15',
            'status': 'active'
        },
        {
            'name': 'Estación Unicentro',
            'description': 'Estación cerca del centro comercial Unicentro',
            'address': 'Autopista Sur con Calle 5',
            'institution': institutions[0],
            'location': Point(-76.5425, 3.3703, srid=4326),
            'installed_at': '2023-03-20',
            'status': 'active'
        },
        {
            'name': 'Estación Ciudad Jardín',
            'description': 'Estación residencial norte',
            'address': 'Calle 16 Norte #9N-35',
            'institution': institutions[1],
            'location': Point(-76.5378, 3.4632, srid=4326),
            'installed_at': '2023-06-10',
            'status': 'active'
        },
        {
            'name': 'Estación Universidad del Valle',
            'description': 'Estación académica',
            'address': 'Ciudad Universitaria Meléndez',
            'institution': institutions[2],
            'location': Point(-76.5321, 3.3756, srid=4326),
            'installed_at': '2023-02-01',
            'status': 'active'
        },
        {
            'name': 'Estación Aguablanca',
            'description': 'Estación en zona oriental',
            'address': 'Carrera 15 con Calle 70',
            'institution': institutions[1],
            'location': Point(-76.4892, 3.4123, srid=4326),
            'installed_at': '2023-08-15',
            'status': 'maintenance'
        }
    ]

    for data in station_data:
        station, created = Station.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'address': data['address'],
                'institution': data['institution'],
                'admin': admin,
                'location': data['location'],
                'installed_at': data['installed_at'],
                'status': data['status']
            }
        )
        if created:
            print(f"  ✓ Station: {station.name} ({station.status})")
        stations.append(station)

    return stations


def create_devices(stations):
    """Create sample devices for each station.

    Args:
        stations (list): List of Station instances

    Returns:
        list: List of Device instances
    """
    print("\n🔬 Creating devices...")

    devices = []

    for station in stations:
        # PM2.5 sensor
        device, created = Device.objects.get_or_create(
            serial_number=f'PM25-{station.id:03d}',
            defaults={
                'description': 'PM2.5 sensor',
                'type': 'SENSOR',
                'station': station
            }
        )
        if created:
            print(f"  ✓ Device: {device.serial_number} in {station.name}")
            devices.append(device)

        # NO2 sensor
        device, created = Device.objects.get_or_create(
            serial_number=f'NO2-{station.id:03d}',
            defaults={
                'description': 'NO2 sensor',
                'type': 'SENSOR',
                'station': station
            }
        )
        if created:
            devices.append(device)

        # Weather station
        device, created = Device.objects.get_or_create(
            serial_number=f'METEO-{station.id:03d}',
            defaults={
                'description': 'Weather station',
                'type': 'METEO',
                'station': station
            }
        )
        if created:
            devices.append(device)

    return devices


def create_alerts(stations):
    """Create sample alerts with pollutants.

    Args:
        stations (list): List of Station instances

    Returns:
        list: List of Alert instances
    """
    print("\n Creating alerts...")

    alerts = []

    # Critical alert at first station
    alert, created = Alert.objects.get_or_create(
        station=stations[0],
        attended=False
    )
    if created:
        AlertPollutant.objects.create(alert=alert, pollutant='PM25', level=75.5)
        AlertPollutant.objects.create(alert=alert, pollutant='NO2', level=65.2)
        print(f"  ✓ Critical alert at {stations[0].name}")
        alerts.append(alert)

    # Moderate alert at second station
    alert, created = Alert.objects.get_or_create(
        station=stations[1],
        attended=True
    )
    if created:
        AlertPollutant.objects.create(alert=alert, pollutant='O3', level=45.3)
        print(f"  ✓ Alert (attended) at {stations[1].name}")
        alerts.append(alert)

    return alerts


def main():
    """Main function to execute all seed tasks."""
    print("=" * 60)
    print(" VRISA - Seed Data Script")
    print("=" * 60)

    try:
        # Users
        admin_user, researcher_user, citizen_user = create_users()

        # Profiles
        admin = create_admin_profiles(admin_user)
        auth_user = create_auth_users(researcher_user)

        # Institutions
        institutions = create_institutions(admin)

        # Stations
        stations = create_stations(institutions, admin)

        # Devices
        devices = create_devices(stations)

        # Alerts
        alerts = create_alerts(stations)

        # Summary
        print("\n" + "=" * 60)
        print(" SUMMARY:")
        print(f"  - Users: {User.objects.count()}")
        print(f"  - Admins: {Admin.objects.count()}")
        print(f"  - AuthUsers: {AuthUser.objects.count()}")
        print(f"  - Institutions: {Institution.objects.count()}")
        print(f"  - Stations: {Station.objects.count()}")
        print(f"  - Devices: {Device.objects.count()}")
        print(f"  - Alerts: {Alert.objects.count()}")
        print("=" * 60)
        print(" Data loaded successfully!")

        # Test credentials
        print("\n TEST CREDENTIALS:")
        print("  Admin:")
        print("    Email: admin@vrisa.com")
        print("    Password: admin123")
        print("  Researcher:")
        print("    Email: researcher@vrisa.com")
        print("    Password: researcher123")
        print("  Citizen:")
        print("    Email: citizen@vrisa.com")
        print("    Password: citizen123")
        print("=" * 60)

    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()