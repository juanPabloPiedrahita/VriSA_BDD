from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.cache import cache

def test_redis(request):
    cache.set('test_key', 'Hello Redis!', 30)
    value = cache.get('test_key')
    return JsonResponse({'redis_test': value})

#Apartir de aqui se desarrolla un Endpoint temporal para probar sistema entero
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from .models import User

def health_check(request):
    result = {
        'django': 'ok',
        'database': None,
        'redis': None,
        'postgis': None,
    }
    
    # Test PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result['database'] = 'ok'
    except Exception as e:
        result['database'] = str(e)
    
    # Test PostGIS
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_version()")
            result['postgis'] = cursor.fetchone()[0]
    except Exception as e:
        result['postgis'] = str(e)
    
    # Test Redis
    try:
        cache.set('health', 'ok', 10)
        if cache.get('health') == 'ok':
            result['redis'] = 'ok'
    except Exception as e:
        result['redis'] = str(e)
    
    return JsonResponse(result)