from django.contrib import admin
from django.contrib.gis import admin as geoadmin

from .models import (
    User, Admin, AuthUser,
    Institution, Station, Device,
    Alert, AlertPollutant,
    AlertReceive, StationConsult
)

# -------------------------
# Custom User Admin
# -------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", "is_staff", "is_active", "created_at")
    search_fields = ("name", "email")
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


# -------------------------
# Admin Profile
# -------------------------
@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "access_level", "created_at")
    search_fields = ("user__email", "user__name")


# -------------------------
# AuthUser Profile
# -------------------------
@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "read_access", "created_at")
    search_fields = ("user__email",)


# -------------------------
# Institution
# -------------------------
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "verified", "admin", "created_at")
    list_filter = ("verified",)
    search_fields = ("name", "admin__user__email")


# -------------------------
# Station (GeoModelAdmin)
# -------------------------
@admin.register(Station)
class StationAdmin(geoadmin.GeoModelAdmin):
    list_display = ("id", "name", "institution", "admin", "status", "installed_at")
    search_fields = ("name", "institution__name", "admin__user__email")
    list_filter = ("status",)
    readonly_fields = ("created_at", "updated_at")


# -------------------------
# Device
# -------------------------
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "serial_number", "type", "station", "install_date")
    list_filter = ("type",)
    search_fields = ("serial_number",)


# -------------------------
# Alert
# -------------------------
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "station", "attended", "alert_date")
    list_filter = ("attended", "station")
    search_fields = ("station__name",)


# -------------------------
# AlertPollutant
# -------------------------
@admin.register(AlertPollutant)
class AlertPollutantAdmin(admin.ModelAdmin):
    list_display = ("id", "alert", "pollutant", "level", "recorded_at")
    list_filter = ("pollutant",)
    search_fields = ("alert__station__name",)


# -------------------------
# M2M intermediate tables
# -------------------------
@admin.register(AlertReceive)
class AlertReceiveAdmin(admin.ModelAdmin):
    list_display = ("id", "auth_user", "alert", "received_at")
    search_fields = ("auth_user__user__email", "alert__station__name")


@admin.register(StationConsult)
class StationConsultAdmin(admin.ModelAdmin):
    list_display = ("id", "auth_user", "station", "granted_at")
    search_fields = ("auth_user__user__email", "station__name")
