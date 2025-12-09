"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from api.views import test_redis
from api.views import health_check  #Importa la view de health_check, para el endpoint de verificacion de salud

def health_check(request):
    """Simple health check endpoint"""
    from django.db import connection
    from django.core.cache import cache
    
    result = {
        'status': 'ok',
        'django': 'ok',
        'database': None,
        'redis': None,
    }
    
    # Test PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result['database'] = 'ok'
    except Exception as e:
        result['database'] = str(e)
        result['status'] = 'error'
    
    # Test Redis
    try:
        cache.set('health', 'ok', 10)
        if cache.get('health') == 'ok':
            result['redis'] = 'ok'
    except Exception as e:
        result['redis'] = str(e)
    
    return JsonResponse(result)


def api_root(request):
    """API root with links to all endpoints"""
    return JsonResponse({
        'message': 'VRISA API v1.0',
        'documentation': '/api/docs/',
        'endpoints': {
            'health': '/health/',
            'admin': '/admin/',
            'auth': {
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
                'register': '/api/auth/register/',
                'logout': '/api/auth/logout/',
                'change_password': '/api/auth/change-password/',
                'verify': '/api/auth/verify/',
            },
            'resources': {
                'users': '/api/users/',
                'admins': '/api/admins/',
                'auth_users': '/api/auth-users/',
                'institutions': '/api/institutions/',
                'stations': '/api/stations/',
                'devices': '/api/devices/',
                'alerts': '/api/alerts/',
                'alert_pollutants': '/api/alert-pollutants/',
                'alert_receives': '/api/alert-receives/',
                'station_consults': '/api/station-consults/',
            },
            'special_actions': {
                'add_pollutants_to_alert': '/api/alerts/{id}/pollutants/',
                'get_station_alerts': '/api/stations/{id}/alerts/',
                'grant_station_access': '/api/stations/{id}/grant-access/',
                'nearby_stations': '/api/stations/nearby/?lat=X&lon=Y&radius=Z',
                'mark_alert_attended': '/api/alerts/{id}/mark-attended/',
                'notify_alert_users': '/api/alerts/{id}/notify/',
            }
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls), #Sitio de administracion de Django
    path('test-redis/', test_redis), #Endpoint para probar la conexion con Redis
    path('health/', health_check, name='health_check'), #Endpoint para verificar la salud del servicio
    path('', api_root, name='api_root'), #API root
    path('api/', include('api.urls')), #API endpoints
    path('api-auth/', include('rest_framework.urls')), #DRF browsable API auth (para desarrollo)
]
