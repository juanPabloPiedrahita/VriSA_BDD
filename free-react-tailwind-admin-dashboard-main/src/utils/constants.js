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
