import api from './api.config';
import { Alert, AlertPollutant, PaginatedResponse } from '../types/api.types';

export const alertsService = {
  getAll: async (params?: {
    page?: number;
    attended?: boolean;
    station?: number;
    date_after?: string;
  }): Promise<PaginatedResponse<Alert>> => {
    const response = await api.get<PaginatedResponse<Alert>>('/alerts/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Alert> => {
    const response = await api.get<Alert>(`/alerts/${id}/`);
    return response.data;
  },

  addPollutants: async (
    alertId: number,
    pollutants: { pollutant: string; level: number }[]
  ): Promise<AlertPollutant[]> => {
    const response = await api.post<AlertPollutant[]>(`/alerts/${alertId}/pollutants/`, {
      pollutants,
    });
    return response.data;
  },

  markAttended: async (id: number): Promise<Alert> => {
    const response = await api.post<Alert>(`/alerts/${id}/mark-attended/`);
    return response.data;
  },
};