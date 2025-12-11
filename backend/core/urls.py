"""
Root URL configuration for the VRISA Core project.

This module defines the main URL routing for the entire system, including:
- Admin site
- Health check endpoint
- Redis test endpoint
- API root descriptor
- Versioned API routes
- DRF authentication routes (for development)

Structure:
    /admin/              -> Django admin panel
    /test-redis/         -> Redis connectivity test
    /health/             -> System health check (PostgreSQL + Redis)
    /                    -> API root summary
    /api/                -> Main API endpoints (via api.urls)
    /api-auth/           -> DRF login/logout UI

Each endpoint returns a JSON response suitable for monitoring, debugging, or
service discovery.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from api.views import test_redis
from api.views import health_check  # Health check view for service verification


def health_check(request):
    """
    Global system health check.

    Performs quick diagnostics on:
    - Django runtime
    - PostgreSQL connectivity
    - Redis cache availability

    Returns:
        JsonResponse with keys:
        {
            "status": "ok" | "error",
            "django": "ok",
            "database": "ok" | "<error>",
            "redis": "ok" | "<error>"
        }
    """
    from django.db import connection
    from django.core.cache import cache

    result = {
        "status": "ok",
        "django": "ok",
        "database": None,
        "redis": None,
    }

    # PostgreSQL check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result["database"] = "ok"
    except Exception as e:
        result["database"] = str(e)
        result["status"] = "error"

    # Redis check
    try:
        cache.set("health", "ok", 10)
        if cache.get("health") == "ok":
            result["redis"] = "ok"
    except Exception as e:
        result["redis"] = str(e)

    return JsonResponse(result)


def api_root(request):
    """
    API root endpoint.

    Provides a high-level overview of the available API sections and key routes.

    Returns:
        JsonResponse summarizing documentation links, authentication endpoints,
        main resources, and specialized actions.
    """
    return JsonResponse({
        "message": "VRISA API v1.0",
        "documentation": "/api/docs/",
        "endpoints": {
            "health": "/health/",
            "admin": "/admin/",
            "auth": {
                "login": "/api/auth/login/",
                "refresh": "/api/auth/refresh/",
                "register": "/api/auth/register/",
                "logout": "/api/auth/logout/",
                "change_password": "/api/auth/change-password/",
                "verify": "/api/auth/verify/",
            },
            "resources": {
                "users": "/api/users/",
                "admins": "/api/admins/",
                "auth_users": "/api/auth-users/",
                "institutions": "/api/institutions/",
                "stations": "/api/stations/",
                "devices": "/api/devices/",
                "alerts": "/api/alerts/",
                "alert_pollutants": "/api/alert-pollutants/",
                "alert_receives": "/api/alert-receives/",
                "station_consults": "/api/station-consults/",
            },
            "special_actions": {
                "add_pollutants_to_alert": "/api/alerts/{id}/pollutants/",
                "get_station_alerts": "/api/stations/{id}/alerts/",
                "grant_station_access": "/api/stations/{id}/grant-access/",
                "nearby_stations": "/api/stations/nearby/?lat=X&lon=Y&radius=Z",
                "mark_alert_attended": "/api/alerts/{id}/mark-attended/",
                "notify_alert_users": "/api/alerts/{id}/notify/",
            },
        }
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("test-redis/", test_redis),
    path("health/", health_check, name="health_check"),
    path("", api_root, name="api_root"),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
