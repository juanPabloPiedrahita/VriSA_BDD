export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  created_at: string;
  updated_at: string;
  is_admin: boolean;
  is_auth_user: boolean;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface Station {
  id: number;
  name: string;
  description?: string;
  address?: string;
  institution: number;
  institution_name: string;
  admin_name?: string;
  location: {
    type: string;
    coordinates: [number, number]; // [lon, lat]
  };
  status: 'active' | 'inactive' | 'maintenance';
  installed_at?: string;
  devices_count: number;
  alerts_count: number;
  created_at: string;
  updated_at: string;
}

export interface Alert {
  id: number;
  station: number;
  station_name: string;
  alert_date: string;
  attended: boolean;
  pollutants: AlertPollutant[];
  created_at: string;
}

export interface AlertPollutant {
  id: number;
  pollutant: 'PM25' | 'PM10' | 'NO2' | 'O3' | 'SO2' | 'CO';
  level: number;
  recorded_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  total_pages: number;
  current_page: number;
  results: T[];
}

export interface Institution {
  id: number;
  name: string;
  address?: string;
  verified: boolean;
  admin: number;
  admin_name: string;
  stations_count: number;
  created_at: string;
}