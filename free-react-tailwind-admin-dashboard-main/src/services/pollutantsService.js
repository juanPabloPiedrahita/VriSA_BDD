// Servicio para datos de contaminantes
import api from './api';

export const pollutantsService = {
  getLatest: (stationId) => api.get(`/pollutants/latest/${stationId}/`),
  getHistorical: (stationId, params) => api.get(`/pollutants/historical/${stationId}/`, { params }),
};
