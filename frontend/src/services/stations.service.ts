import api from './api.config';
import { Station, Alert, PaginatedResponse } from '../types/api.types';

export const stationsService = {
  getAll: async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    status?: string;
  }): Promise<PaginatedResponse<Station>> => {
    const response = await api.get<PaginatedResponse<Station>>('/stations/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Station> => {
    const response = await api.get<Station>(`/stations/${id}/`);
    return response.data;
  },

  create: async (stationData: {
    name: string;
    description?: string;
    address?: string;
    institution: number;
    admin?: number;
    location: [number, number]; // [lon, lat]
    status?: string;
    installed_at?: string;
  }): Promise<Station> => {
    const response = await api.post<Station>('/stations/', stationData);
    return response.data;
  },

  update: async (id: number, stationData: Partial<Station>): Promise<Station> => {
    const response = await api.put<Station>(`/stations/${id}/`, stationData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/stations/${id}/`);
  },

  getAlerts: async (id: number, params?: { attended?: boolean }): Promise<PaginatedResponse<Alert>> => {
    const response = await api.get<PaginatedResponse<Alert>>(`/stations/${id}/alerts/`, { params });
    return response.data;
  },

  getNearby: async (lat: number, lon: number, radius = 5000): Promise<Station[]> => {
    const response = await api.get<Station[]>('/stations/nearby/', {
      params: { lat, lon, radius },
    });
    return response.data;
  },
};