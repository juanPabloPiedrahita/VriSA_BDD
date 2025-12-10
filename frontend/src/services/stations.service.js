import api from './api';

export const stationsService = {
  // Get all stations
  getAll: async (params = {}) => {
    const response = await api.get('/stations/', { params });
    return response.data;
  },

  // Get station by ID
  getById: async (id) => {
    const response = await api.get(`/stations/${id}/`);
    return response.data;
  },

  // Create station
  create: async (stationData) => {
    const response = await api.post('/stations/', stationData);
    return response.data;
  },

  // Update station
  update: async (id, stationData) => {
    const response = await api.put(`/stations/${id}/`, stationData);
    return response.data;
  },

  // Delete station
  delete: async (id) => {
    await api.delete(`/stations/${id}/`);
  },

  // Get station alerts
  getAlerts: async (id, params = {}) => {
    const response = await api.get(`/stations/${id}/alerts/`, { params });
    return response.data;
  },

  // Get nearby stations
  getNearby: async (lat, lon, radius = 5000) => {
    const response = await api.get('/stations/nearby/', {
      params: { lat, lon, radius },
    });
    return response.data;
  },
};