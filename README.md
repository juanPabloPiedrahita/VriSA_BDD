# VRISA - Sistema de Monitoreo de Calidad del Aire

**V**igilancia de **R**iesgos y **S**ustancias **A**tmosféricas

Sistema de monitoreo ambiental para la calidad del aire en la ciudad de Cali. Permite la recolección, procesamiento, almacenamiento y visualización de datos de estaciones de monitoreo distribuidas que miden contaminantes atmosféricos y variables meteorológicas en tiempo real.

---

## 📋 Tabla de Contenidos

* [Descripción del Proyecto](#-descripci%C3%B3n-del-proyecto)
* [Stack Tecnológico](#-stack-tecnol%C3%B3gico)
* [Arquitectura](#-arquitectura)
* [Requisitos Previos](#-requisitos-previos)
* [Instalación y Configuración](#-instalaci%C3%B3n-y-configuraci%C3%B3n)
* [Uso del Sistema](#-uso-del-sistema)
* [API Endpoints](#-api-endpoints)
* [Testing](#-testing)
* [Estructura del Proyecto](#-estructura-del-proyecto)
* [Equipo](#-equipo)

---

## 🎯 Descripción del Proyecto

VRISA es una plataforma de monitoreo ambiental que permite:

* 🏢 **Gestión de instituciones** que operan estaciones de calidad del aire
* 📍 **Registro de estaciones** con geolocalización (PostGIS)
* 🔬  **Monitoreo de contaminantes** : PM2.5, PM10, SO₂, NO₂, O₃, CO
* 🌡️  **Variables meteorológicas** : temperatura, humedad, velocidad del viento
* 🚨 **Sistema de alertas** configurables por umbrales de contaminantes
* 👥 **Control de acceso** por roles (admin, usuario autorizado, público)
* 📊 **Consultas espaciales** (estaciones cercanas usando PostGIS)
* 🔐 **Autenticación JWT** segura

---

## 🛠️ Stack Tecnológico

### Backend

* **Django 4.2** - Framework web
* **Django REST Framework** - API REST
* **PostgreSQL 15 + PostGIS** - Base de datos con extensión espacial
* **Redis 7** - Cache y sesiones
* **JWT** - Autenticación token-based
* **Docker & Docker Compose** - Containerización

### Frontend (En desarrollo)

* **React** - Aplicación web
* **Expo** - Aplicación móvil

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    VRISA Architecture                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Frontend   │      │   Mobile     │                │
│  │   (React)    │◄────►│   (Expo)     │                │
│  └──────┬───────┘      └──────┬───────┘                │
│         │                     │                         │
│         └─────────┬───────────┘                         │
│                   │                                     │
│              HTTP/REST                                  │
│                   │                                     │
│         ┌─────────▼────────────┐                       │
│         │   Django Backend     │                       │
│         │  (REST Framework)    │                       │
│         │   + JWT Auth         │                       │
│         └─────────┬────────────┘                       │
│                   │                                     │
│         ┌─────────┴────────────┐                       │
│         │                      │                       │
│   ┌─────▼─────┐         ┌─────▼─────┐                │
│   │ PostgreSQL│         │   Redis   │                │
│   │ + PostGIS │         │   Cache   │                │
│   └───────────┘         └───────────┘                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Modelos de Datos Principales

```
User (auth)
  │
  ├── Admin (1:1)
  │     └── Institution (1:N)
  │           └── Station (1:N)
  │                 ├── Device (1:N)
  │                 └── Alert (1:N)
  │                       └── AlertPollutant (1:N)
  │
  └── AuthUser (1:1)
        ├── StationConsult (M:N with Station)
        └── AlertReceive (M:N with Alert)
```

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

* **Docker** >= 20.10
* **Docker Compose** >= 2.0
* **Git**
* **jq** (para testing): `sudo apt-get install jq` o `brew install jq`

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd VRISA
```

### 2. Estructura de directorios

```
VRISA/
├── backend/           # Django Backend
│   ├── api/          # App principal
│   ├── core/         # Configuración Django
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          # React Frontend (por desarrollar)
├── infra/            # Docker Compose
│   ├── docker-compose.yml
│   └── vrisa_test_script.sh
└── README.md
```

### 3. Configurar variables de entorno (opcional)

Si necesitas cambiar configuraciones, crea un archivo `.env` en `infra/`:

```bash
# infra/.env
POSTGRES_DB=vrisa
POSTGRES_USER=vrisa_user
POSTGRES_PASSWORD=vrisa_pass
DJANGO_SECRET_KEY=tu-secret-key-aqui
```

### 4. Construir y levantar los servicios

```bash
cd infra/

# Construir las imágenes (primera vez o después de cambios)
docker compose build

# Levantar todos los servicios
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f
```

**Servicios levantados:**

* 🐘 **PostgreSQL** (PostGIS): `localhost:5432`
* 🔴  **Redis** : `localhost:6379`
* 🐍  **Django Backend** : `http://localhost:8000`
* ⚛️  **React Frontend** : `http://localhost:3000` (cuando esté implementado)

### 5. Aplicar migraciones (primera vez)

```bash
# Verificar que los contenedores están corriendo
docker compose ps

# Aplicar migraciones
docker compose exec backend python manage.py migrate

# Crear superusuario (opcional)
docker compose exec backend python manage.py createsuperuser
```

Ingresa:

* **Email** : `admin@vrisa.com`
* **Name** : `Admin VRISA`
* **Password** : `admin123` (o el que prefieras)

---

## 💻 Uso del Sistema

### Acceder al Backend

* **API Root** : http://localhost:8000
* **Django Admin** : http://localhost:8000/admin
* **API Endpoints** : http://localhost:8000/api/
* **Health Check** : http://localhost:8000/health/

### Detener los servicios

```bash
docker compose down
```

### Reiniciar un servicio específico

```bash
docker compose restart backend
```

### Ver logs de un servicio

```bash
docker compose logs -f backend
docker compose logs -f db
```

### Resetear todo (incluye datos)

```bash
docker compose down -v  # -v elimina los volúmenes (datos)
docker compose up --build
```

---

## 🔌 API Endpoints

### Autenticación

| Método  | Endpoint                       | Descripción                |
| -------- | ------------------------------ | --------------------------- |
| `POST` | `/api/auth/register/`        | Registrar nuevo usuario     |
| `POST` | `/api/auth/login/`           | Login (obtener JWT tokens)  |
| `POST` | `/api/auth/refresh/`         | Refrescar access token      |
| `POST` | `/api/auth/logout/`          | Logout (blacklist token)    |
| `GET`  | `/api/auth/verify/`          | Verificar validez del token |
| `POST` | `/api/auth/change-password/` | Cambiar contraseña         |

### Usuarios

| Método  | Endpoint             | Descripción    | Auth     |
| -------- | -------------------- | --------------- | -------- |
| `GET`  | `/api/users/`      | Listar usuarios | Admin    |
| `POST` | `/api/users/`      | Crear usuario   | Público |
| `GET`  | `/api/users/me/`   | Usuario actual  | Auth     |
| `GET`  | `/api/users/{id}/` | Detalle usuario | Admin    |

### Estaciones

| Método  | Endpoint                                       | Descripción             | Auth  |
| -------- | ---------------------------------------------- | ------------------------ | ----- |
| `GET`  | `/api/stations/`                             | Listar estaciones        | Auth  |
| `POST` | `/api/stations/`                             | Crear estación          | Admin |
| `GET`  | `/api/stations/{id}/`                        | Detalle estación        | Auth  |
| `GET`  | `/api/stations/{id}/alerts/`                 | Alertas de una estación | Auth  |
| `GET`  | `/api/stations/nearby/?lat=X&lon=Y&radius=Z` | Estaciones cercanas      | Auth  |
| `POST` | `/api/stations/{id}/grant-access/`           | Dar acceso a usuario     | Admin |

### Alertas

| Método  | Endpoint                            | Descripción          | Auth  |
| -------- | ----------------------------------- | --------------------- | ----- |
| `GET`  | `/api/alerts/`                    | Listar alertas        | Auth  |
| `POST` | `/api/alerts/`                    | Crear alerta          | Admin |
| `GET`  | `/api/alerts/{id}/`               | Detalle alerta        | Auth  |
| `POST` | `/api/alerts/{id}/pollutants/`    | Agregar contaminantes | Admin |
| `POST` | `/api/alerts/{id}/mark-attended/` | Marcar como atendida  | Admin |
| `POST` | `/api/alerts/{id}/notify/`        | Notificar usuarios    | Admin |

### Tests Manuales Rápidos

#### 1. Health Check

```bash
curl http://localhost:8000/health/
```

#### 2. Registrar usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123",
    "role": "citizen"
  }'
```

#### 3. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }'
```

Guarda el `access` token para usarlo en las siguientes peticiones.

#### 4. Ver perfil actual

```bash
TOKEN="tu_access_token_aqui"

curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer $TOKEN"
```

#### 5. Listar estaciones

```bash
curl http://localhost:8000/api/stations/ \
  -H "Authorization: Bearer $TOKEN"
```

### Testing desde Django Shell

```bash
docker compose exec backend python manage.py shell
```

```python
# Crear una estación de prueba
from api.models import User, Admin, Institution, Station
from django.contrib.gis.geos import Point

# Obtener o crear admin
admin_user = User.objects.get(email='admin@vrisa.com')
admin = Admin.objects.create(user=admin_user, access_level=5)

# Crear institución
inst = Institution.objects.create(
    name='CAR Cali',
    address='Calle 5 #10-20',
    verified=True,
    admin=admin
)

# Crear estación
station = Station.objects.create(
    name='Estación Centro',
    description='Estación de monitoreo centro de Cali',
    address='Carrera 10 #5-50',
    institution=inst,
    admin=admin,
    location=Point(-76.5319, 3.4516, srid=4326),
    status='active'
)

print(f"Estación creada: {station.name} (ID: {station.id})")
```

---

## 📂 Estructura del Proyecto

### Backend (`backend/`)

```
backend/
├── api/                      # App principal
│   ├── migrations/          # Migraciones de base de datos
│   │   └── 0001_initial.py # Migración inicial con DDL
│   ├── models.py           # Modelos de datos
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # ViewSets
│   ├── urls.py             # Rutas API
│   ├── permissions.py      # Permisos personalizados
│   ├── filters.py          # Filtros
│   ├── pagination.py       # Paginación
│   └── auth_backend.py     # Backend de autenticación
├── core/                    # Configuración Django
│   ├── settings.py         # Settings principales
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── Dockerfile
├── manage.py
└── requirements.txt
```

### Infraestructura (`infra/`)

```
infra/
├── docker-compose.yml       # Orquestación de servicios
└── vrisa_test_script.sh     # Script de testing
```

---

## 🔒 Seguridad

### Autenticación JWT

El sistema usa JWT (JSON Web Tokens) para autenticación:

* **Access Token** : Válido por 1 hora
* **Refresh Token** : Válido por 7 días
* Los tokens incluyen información del usuario (email, rol, permisos)

### Roles y Permisos

| Rol                 | Permisos                                  |
| ------------------- | ----------------------------------------- |
| **Citizen**   | Ver datos públicos                       |
| **AuthUser**  | Ver datos + Acceso a estaciones asignadas |
| **Admin**     | CRUD completo de todas las entidades      |
| **Superuser** | Admin panel + Crear otros admins          |

### Variables de Entorno Sensibles

**⚠️ IMPORTANTE:** En producción, cambia:

* `DJANGO_SECRET_KEY`
* Contraseñas de base de datos
* Deshabilita `DEBUG=True`
* Configura `ALLOWED_HOSTS`

---

## 🐛 Troubleshooting

### El backend no inicia

```bash
# Verifica logs
docker compose logs backend

# Reinicia el servicio
docker compose restart backend
```

### Error de conexión a la base de datos

```bash
# Verifica que PostgreSQL esté corriendo
docker compose ps

# Reinicia la DB
docker compose restart db

# Espera 10 segundos y reinicia backend
docker compose restart backend
```

### Migraciones desactualizadas

```bash
docker compose exec backend python manage.py migrate
```

### Resetear la base de datos completamente

```bash
docker compose down -v
docker compose up -d db redis
sleep 10
docker compose run --rm backend python manage.py migrate
docker compose up
```

---

## 📚 Recursos Adicionales

* [Django Documentation](https://docs.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [PostGIS Documentation](https://postgis.net/documentation/)
* [JWT.io](https://jwt.io/) - Decodificar tokens

---

## 🚧 Estado del Desarrollo

### ✅ Completado (Backend)

* [X] Arquitectura base con Docker
* [X] Modelos de datos
* [X] API REST completa
* [X] Autenticación JWT
* [X] Sistema de permisos por roles
* [X] Endpoints CRUD para todas las entidades
* [X] Filtros, búsqueda y paginación
* [X] Queries espaciales con PostGIS
* [X] Sistema de alertas

### 🚧 En Desarrollo

* [ ] Frontend React
* [ ] Aplicación móvil (Expo)
* [ ] Dashboard de visualización
* [ ] Sistema de notificaciones en tiempo real
* [ ] Ingesta de datos desde sensores
* [ ] Reportes y exportación de datos

## 👥 Equipo

**Proyecto final - Curso de Bases de Datos**

* **Desarrolladores Backend** : Juan Pablo Piedrahita Triana, Emmanuel Páez Hurtado y David Taborda Montenegro.
* **Desarrolladores Frontend** : Óscar Andrés Rengifo Bustos, Juan David López Jiménez y Hugo Alexander Eraso Rosero.
* **Institución** : Universidad del Valle.
* **Fecha** : Diciembre 2025.

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico.

---

## 🙏 Agradecimientos

* Profesor Jefferson Amado Peña Torres.

---

Todo el trabajo se encuentra en este repositorio, junto con su informe en PDF, y en el siguiente enlace de YouTube: https://youtu.be/KrSPzm1ClQ4?si=SHNDgie9dIWkPirB

---

**¡Disfruta desarrollando VRISA! 🌱🌍**
