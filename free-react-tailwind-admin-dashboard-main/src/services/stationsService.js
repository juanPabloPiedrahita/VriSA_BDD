// Servicio para gestion de estaciones
import api from './api';

export const stationsService = {
  getAll: () => api.get('/stations/'),
  getById: (id) => api.get(`/stations/${id}/`),
  create: (data) => api.post('/stations/', data),
  update: (id, data) => api.put(`/stations/${id}/`, data),
  delete: (id) => api.delete(`/stations/${id}/`),
};
