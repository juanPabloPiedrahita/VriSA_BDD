# Script para crear la estructura de carpetas del proyecto VRISA
# Ejecutar en PowerShell dentro de la carpeta del proyecto TailAdmin

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Creando estructura para VRISA  " -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en la carpeta correcta
if (-not (Test-Path "package.json")) {
    Write-Host "ERROR: No se encuentra package.json" -ForegroundColor Red
    Write-Host "Asegurate de ejecutar este script dentro de la carpeta de TailAdmin" -ForegroundColor Yellow
    exit 1
}

# Crear estructura de carpetas
$folders = @(
    "src/components/Maps",
    "src/components/Charts",
    "src/components/Dashboard",
    "src/components/Stations",
    "src/components/Institutions",
    "src/pages",
    "src/services",
    "src/utils",
    "src/context"
)

Write-Host "Creando carpetas..." -ForegroundColor Green

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "  checkmark Creado: $folder" -ForegroundColor Gray
    } else {
        Write-Host "  arrow Existe: $folder" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Creando archivos base..." -ForegroundColor Green

# Components/Maps
$content = @"
// Componente para mostrar el mapa de estaciones de VRISA
import React from 'react';

const StationsMap = () => {
  return (
    <div>
      {/* Mapa de estaciones aqui */}
    </div>
  );
};

export default StationsMap;
"@
Set-Content -Path "src/components/Maps/StationsMap.jsx" -Value $content -Encoding UTF8

$content = @"
// Componente para marcador individual de estacion
import React from 'react';

const StationMarker = ({ station }) => {
  return null;
};

export default StationMarker;
"@
Set-Content -Path "src/components/Maps/StationMarker.jsx" -Value $content -Encoding UTF8

# Components/Charts
$content = @"
// Componente para grafico de contaminantes
import React from 'react';

const PollutantChart = () => {
  return (
    <div>
      {/* Grafico de contaminantes */}
    </div>
  );
};

export default PollutantChart;
"@
Set-Content -Path "src/components/Charts/PollutantChart.jsx" -Value $content -Encoding UTF8

$content = @"
// Componente para grafico de tendencias
import React from 'react';

const TrendChart = () => {
  return (
    <div>
      {/* Grafico de tendencias */}
    </div>
  );
};

export default TrendChart;
"@
Set-Content -Path "src/components/Charts/TrendChart.jsx" -Value $content -Encoding UTF8

$content = @"
// Componente para grafico de variables meteorologicas
import React from 'react';

const MeteorologicalChart = () => {
  return (
    <div>
      {/* Grafico meteorologico */}
    </div>
  );
};

export default MeteorologicalChart;
"@
Set-Content -Path "src/components/Charts/MeteorologicalChart.jsx" -Value $content -Encoding UTF8

# Components/Dashboard
$content = @"
// Tarjeta de calidad del aire
import React from 'react';

const AirQualityCard = () => {
  return (
    <div>
      {/* Tarjeta de calidad del aire */}
    </div>
  );
};

export default AirQualityCard;
"@
Set-Content -Path "src/components/Dashboard/AirQualityCard.jsx" -Value $content -Encoding UTF8

$content = @"
// Panel de alertas
import React from 'react';

const AlertsPanel = () => {
  return (
    <div>
      {/* Panel de alertas */}
    </div>
  );
};

export default AlertsPanel;
"@
Set-Content -Path "src/components/Dashboard/AlertsPanel.jsx" -Value $content -Encoding UTF8

$content = @"
// Estado de estaciones
import React from 'react';

const StationStatus = () => {
  return (
    <div>
      {/* Estado de estaciones */}
    </div>
  );
};

export default StationStatus;
"@
Set-Content -Path "src/components/Dashboard/StationStatus.jsx" -Value $content -Encoding UTF8

# Components/Stations
$content = @"
// Lista de estaciones
import React from 'react';

const StationsList = () => {
  return (
    <div>
      {/* Lista de estaciones */}
    </div>
  );
};

export default StationsList;
"@
Set-Content -Path "src/components/Stations/StationsList.jsx" -Value $content -Encoding UTF8

$content = @"
// Formulario para crear/editar estacion
import React from 'react';

const StationForm = () => {
  return (
    <div>
      {/* Formulario de estacion */}
    </div>
  );
};

export default StationForm;
"@
Set-Content -Path "src/components/Stations/StationForm.jsx" -Value $content -Encoding UTF8

$content = @"
// Detalles de estacion
import React from 'react';

const StationDetails = () => {
  return (
    <div>
      {/* Detalles de estacion */}
    </div>
  );
};

export default StationDetails;
"@
Set-Content -Path "src/components/Stations/StationDetails.jsx" -Value $content -Encoding UTF8

# Components/Institutions
$content = @"
// Lista de instituciones
import React from 'react';

const InstitutionsList = () => {
  return (
    <div>
      {/* Lista de instituciones */}
    </div>
  );
};

export default InstitutionsList;
"@
Set-Content -Path "src/components/Institutions/InstitutionsList.jsx" -Value $content -Encoding UTF8

$content = @"
// Formulario de institucion
import React from 'react';

const InstitutionForm = () => {
  return (
    <div>
      {/* Formulario de institucion */}
    </div>
  );
};

export default InstitutionForm;
"@
Set-Content -Path "src/components/Institutions/InstitutionForm.jsx" -Value $content -Encoding UTF8

# Pages
$content = @"
// Dashboard principal de VRISA
import React from 'react';

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard VRISA</h1>
    </div>
  );
};

export default Dashboard;
"@
Set-Content -Path "src/pages/Dashboard.jsx" -Value $content -Encoding UTF8

$content = @"
// Pagina de gestion de estaciones
import React from 'react';

const Stations = () => {
  return (
    <div>
      <h1>Gestion de Estaciones</h1>
    </div>
  );
};

export default Stations;
"@
Set-Content -Path "src/pages/Stations.jsx" -Value $content -Encoding UTF8

$content = @"
// Pagina de reportes
import React from 'react';

const Reports = () => {
  return (
    <div>
      <h1>Reportes</h1>
    </div>
  );
};

export default Reports;
"@
Set-Content -Path "src/pages/Reports.jsx" -Value $content -Encoding UTF8

$content = @"
// Pagina de alertas
import React from 'react';

const Alerts = () => {
  return (
    <div>
      <h1>Sistema de Alertas</h1>
    </div>
  );
};

export default Alerts;
"@
Set-Content -Path "src/pages/Alerts.jsx" -Value $content -Encoding UTF8

$content = @"
// Pagina de configuracion
import React from 'react';

const Settings = () => {
  return (
    <div>
      <h1>Configuracion</h1>
    </div>
  );
};

export default Settings;
"@
Set-Content -Path "src/pages/Settings.jsx" -Value $content -Encoding UTF8

# Services
$content = @"
// Configuracion base de Axios para la API
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = ``Bearer `${token}``;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
"@
Set-Content -Path "src/services/api.js" -Value $content -Encoding UTF8

$content = @"
// Servicio para gestion de estaciones
import api from './api';

export const stationsService = {
  getAll: () => api.get('/stations/'),
  getById: (id) => api.get(``/stations/`${id}/``),
  create: (data) => api.post('/stations/', data),
  update: (id, data) => api.put(``/stations/`${id}/``, data),
  delete: (id) => api.delete(``/stations/`${id}/``),
};
"@
Set-Content -Path "src/services/stationsService.js" -Value $content -Encoding UTF8

$content = @"
// Servicio para datos de contaminantes
import api from './api';

export const pollutantsService = {
  getLatest: (stationId) => api.get(``/pollutants/latest/`${stationId}/``),
  getHistorical: (stationId, params) => api.get(``/pollutants/historical/`${stationId}/``, { params }),
};
"@
Set-Content -Path "src/services/pollutantsService.js" -Value $content -Encoding UTF8

$content = @"
// Servicio de autenticacion
import api from './api';

export const authService = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getCurrentUser: () => api.get('/auth/user/'),
};
"@
Set-Content -Path "src/services/authService.js" -Value $content -Encoding UTF8

# Utils
$content = @"
// Constantes del proyecto VRISA
export const POLLUTANTS = {
  PM25: 'PM2.5',
  PM10: 'PM10',
  SO2: 'SO2',
  NO2: 'NO2',
  O3: 'O3',
  CO: 'CO',
};

export const AQI_LEVELS = {
  GOOD: { min: 0, max: 50, color: '#00E400', label: 'Buena' },
  MODERATE: { min: 51, max: 100, color: '#FFFF00', label: 'Moderada' },
  UNHEALTHY_SENSITIVE: { min: 101, max: 150, color: '#FF7E00', label: 'Danina para grupos sensibles' },
  UNHEALTHY: { min: 151, max: 200, color: '#FF0000', label: 'Danina' },
  VERY_UNHEALTHY: { min: 201, max: 300, color: '#8F3F97', label: 'Muy danina' },
  HAZARDOUS: { min: 301, max: 500, color: '#7E0023', label: 'Peligrosa' },
};

export const CALI_CENTER = {
  lat: 3.4516,
  lng: -76.5320,
};
"@
Set-Content -Path "src/utils/constants.js" -Value $content -Encoding UTF8

$content = @"
// Calculo del Indice de Calidad del Aire
export const calculateAQI = (pollutant, concentration) => {
  // Implementar calculo de ICA segun normativa colombiana
  // TODO: Implementar formulas de calculo
  return 0;
};

export const getAQILevel = (aqi) => {
  // TODO: Retornar el nivel segun el valor de AQI
  return null;
};
"@
Set-Content -Path "src/utils/airQualityIndex.js" -Value $content -Encoding UTF8

$content = @"
// Funciones de formato
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO');
};

export const formatDateTime = (date) => {
  return new Date(date).toLocaleString('es-CO');
};

export const formatNumber = (num, decimals = 2) => {
  return Number(num).toFixed(decimals);
};
"@
Set-Content -Path "src/utils/formatters.js" -Value $content -Encoding UTF8

# Context
$content = @"
// Contexto de autenticacion
import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, setUser, setIsAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
"@
Set-Content -Path "src/context/AuthContext.jsx" -Value $content -Encoding UTF8

$content = @"
// Contexto de estaciones
import React, { createContext, useState, useContext } from 'react';

const StationsContext = createContext();

export const StationsProvider = ({ children }) => {
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);

  return (
    <StationsContext.Provider value={{ stations, setStations, selectedStation, setSelectedStation }}>
      {children}
    </StationsContext.Provider>
  );
};

export const useStations = () => useContext(StationsContext);
"@
Set-Content -Path "src/context/StationsContext.jsx" -Value $content -Encoding UTF8

# Crear archivo .env
$content = @"
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MAP_CENTER_LAT=3.4516
REACT_APP_MAP_CENTER_LNG=-76.5320
REACT_APP_MAP_ZOOM=12
"@
Set-Content -Path ".env" -Value $content -Encoding UTF8

Write-Host "  checkmark Archivos base creados" -ForegroundColor Gray

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "  checkmark Estructura creada exitosamente" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "1. Instalar dependencias adicionales:" -ForegroundColor White
Write-Host "   npm install recharts leaflet react-leaflet lucide-react axios date-fns" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Ejecutar el proyecto:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Yellow
Write-Host ""