// PollutionQuery.tsx
import { useState } from "react";
import Badge from "/home/oscar/Documents/BASES_DE_DATOS_2025-2/DASHBOARD_PLANTILLA/free-react-tailwind-admin-dashboard/src/components/ui/badge/Badge.tsx";
import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "/home/oscar/Documents/BASES_DE_DATOS_2025-2/DASHBOARD_PLANTILLA/free-react-tailwind-admin-dashboard/src/components/ui/table/index.tsx";

// Componentes de iconos en línea (para evitar imports)
const SearchIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
);

const FilterIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
  </svg>
);

const CalendarIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const MapPinIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const DownloadIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
  </svg>
);

// Tipos de datos
interface PollutionRecord {
  id: number;
  timestamp: string;
  location: string;
  zone: string;
  pm25: number;
  pm10: number;
  no2: number;
  o3: number;
  so2: number;
  co: number;
  aqi: number;
  status: "Buena" | "Moderada" | "Dañina" | "Muy Dañina" | "Peligrosa";
}

// Datos de ejemplo para Cali
const pollutionData: PollutionRecord[] = [
  {
    id: 1,
    timestamp: "2024-01-15 08:00",
    location: "Centro",
    zone: "Zona 1 - Centro Histórico",
    pm25: 28.5,
    pm10: 42.3,
    no2: 38.7,
    o3: 65.2,
    so2: 12.4,
    co: 1.8,
    aqi: 65,
    status: "Moderada"
  },
  {
    id: 2,
    timestamp: "2024-01-15 10:00",
    location: "Norte",
    zone: "Zona 2 - Versalles",
    pm25: 22.1,
    pm10: 38.5,
    no2: 32.4,
    o3: 58.7,
    so2: 10.2,
    co: 1.5,
    aqi: 58,
    status: "Moderada"
  },
  {
    id: 3,
    timestamp: "2024-01-15 12:00",
    location: "Sur",
    zone: "Zona 3 - Siloé",
    pm25: 32.8,
    pm10: 48.9,
    no2: 42.3,
    o3: 72.1,
    so2: 15.8,
    co: 2.1,
    aqi: 72,
    status: "Moderada"
  },
  {
    id: 4,
    timestamp: "2024-01-15 14:00",
    location: "Este",
    zone: "Zona 4 - Industrial",
    pm25: 45.6,
    pm10: 62.4,
    no2: 55.8,
    o3: 85.3,
    so2: 22.7,
    co: 3.2,
    aqi: 85,
    status: "Dañina"
  },
  {
    id: 5,
    timestamp: "2024-01-15 16:00",
    location: "Oeste",
    zone: "Zona 5 - Universitaria",
    pm25: 18.9,
    pm10: 35.2,
    no2: 28.6,
    o3: 52.4,
    so2: 8.9,
    co: 1.2,
    aqi: 52,
    status: "Moderada"
  },
  {
    id: 6,
    timestamp: "2024-01-14 08:00",
    location: "Centro",
    zone: "Zona 1 - Centro Histórico",
    pm25: 35.2,
    pm10: 52.1,
    no2: 45.8,
    o3: 78.6,
    so2: 18.3,
    co: 2.4,
    aqi: 78,
    status: "Moderada"
  },
  {
    id: 7,
    timestamp: "2024-01-14 12:00",
    location: "Norte",
    zone: "Zona 2 - Versalles",
    pm25: 25.4,
    pm10: 40.8,
    no2: 35.2,
    o3: 62.1,
    so2: 11.5,
    co: 1.7,
    aqi: 62,
    status: "Moderada"
  },
  {
    id: 8,
    timestamp: "2024-01-13 08:00",
    location: "Sur",
    zone: "Zona 3 - Siloé",
    pm25: 38.9,
    pm10: 56.3,
    no2: 48.7,
    o3: 82.4,
    so2: 20.1,
    co: 2.8,
    aqi: 82,
    status: "Dañina"
  },
];

// Ubicaciones disponibles
const locations = [
  { value: "all", label: "Todas las ubicaciones" },
  { value: "Centro", label: "Centro Histórico" },
  { value: "Norte", label: "Norte (Versalles)" },
  { value: "Sur", label: "Sur (Siloé)" },
  { value: "Este", label: "Este (Industrial)" },
  { value: "Oeste", label: "Oeste (Universitaria)" },
];

// Fechas disponibles
const dateRanges = [
  { value: "today", label: "Hoy" },
  { value: "yesterday", label: "Ayer" },
  { value: "week", label: "Última semana" },
  { value: "month", label: "Último mes" },
  { value: "custom", label: "Personalizado" },
];

// Función para obtener color del estado AQI
const getAqiColor = (aqi: number) => {
  if (aqi <= 50) return "success";
  if (aqi <= 100) return "warning";
  if (aqi <= 150) return "error";
  if (aqi <= 200) return "error";
  return "error";
};

// Función para obtener texto del estado AQI
const getAqiStatus = (aqi: number): PollutionRecord["status"] => {
  if (aqi <= 50) return "Buena";
  if (aqi <= 100) return "Moderada";
  if (aqi <= 150) return "Dañina";
  if (aqi <= 200) return "Muy Dañina";
  return "Peligrosa";
};

export default function PollutionQuery() {
  // Estados para los filtros
  const [selectedLocation, setSelectedLocation] = useState("all");
  const [selectedDateRange, setSelectedDateRange] = useState("week");
  const [searchQuery, setSearchQuery] = useState("");
  const [customStartDate, setCustomStartDate] = useState("");
  const [customEndDate, setCustomEndDate] = useState("");
  const [showCustomDate, setShowCustomDate] = useState(false);

  // Manejar cambio de rango de fecha
  const handleDateRangeChange = (value: string) => {
    setSelectedDateRange(value);
    setShowCustomDate(value === "custom");
  };

  // Filtrar datos
  const filteredData = pollutionData.filter(record => {
    // Filtrar por búsqueda
    if (searchQuery && !record.zone.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }

    // Filtrar por ubicación
    if (selectedLocation !== "all" && record.location !== selectedLocation) {
      return false;
    }

    // Filtrar por fecha (simplificado para demo)
    const recordDate = new Date(record.timestamp);
    const now = new Date();
    
    switch (selectedDateRange) {
      case "today":
        return recordDate.toDateString() === now.toDateString();
      case "yesterday":
        const yesterday = new Date(now);
        yesterday.setDate(yesterday.getDate() - 1);
        return recordDate.toDateString() === yesterday.toDateString();
      case "week":
        const weekAgo = new Date(now);
        weekAgo.setDate(weekAgo.getDate() - 7);
        return recordDate >= weekAgo;
      case "month":
        const monthAgo = new Date(now);
        monthAgo.setMonth(monthAgo.getMonth() - 1);
        return recordDate >= monthAgo;
      case "custom":
        if (customStartDate && customEndDate) {
          const start = new Date(customStartDate);
          const end = new Date(customEndDate);
          end.setHours(23, 59, 59, 999);
          return recordDate >= start && recordDate <= end;
        }
        return true;
      default:
        return true;
    }
  });

  // Manejar descarga de datos
  const handleDownload = () => {
    const csvData = [
      ["Fecha", "Ubicación", "Zona", "PM2.5", "PM10", "NO2", "O3", "SO2", "CO", "AQI", "Estado"],
      ...filteredData.map(record => [
        record.timestamp,
        record.location,
        record.zone,
        record.pm25,
        record.pm10,
        record.no2,
        record.o3,
        record.so2,
        record.co,
        record.aqi,
        record.status
      ])
    ];

    const csvContent = csvData.map(row => row.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `contaminacion_cali_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
      {/* Header */}
      <div className="flex flex-col gap-4 mb-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Consulta de Contaminación
          </h3>
          <p className="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
            Filtra registros por fecha y ubicación - Cali, Colombia
          </p>
        </div>
        
        <button
          onClick={handleDownload}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-500 px-4 py-2.5 text-theme-sm font-medium text-white shadow-theme-xs hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
        >
          <DownloadIcon />
          Exportar Datos
        </button>
      </div>

      {/* Filtros */}
      <div className="mb-6 p-4 bg-gray-50 rounded-xl dark:bg-gray-800/50">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
          
          {/* Búsqueda por zona */}
          <div className="flex-1">
            <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              Buscar zona
            </label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                <SearchIcon />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Ej: Centro, Norte, Industrial..."
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-700 placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-500"
              />
            </div>
          </div>

          {/* Filtro por ubicación */}
          <div className="flex-1">
            <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              Ubicación
            </label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                <MapPinIcon />
              </div>
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 appearance-none dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              >
                {locations.map(loc => (
                  <option key={loc.value} value={loc.value}>
                    {loc.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Filtro por fecha */}
          <div className="flex-1">
            <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              Rango de fecha
            </label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                <CalendarIcon />
              </div>
              <select
                value={selectedDateRange}
                onChange={(e) => handleDateRangeChange(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 appearance-none dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              >
                {dateRanges.map(range => (
                  <option key={range.value} value={range.value}>
                    {range.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

        </div>

        {/* Fechas personalizadas */}
        {showCustomDate && (
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
              <div className="flex-1">
                <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                  Fecha inicial
                </label>
                <input
                  type="date"
                  value={customStartDate}
                  onChange={(e) => setCustomStartDate(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                />
              </div>
              <div className="flex-1">
                <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                  Fecha final
                </label>
                <input
                  type="date"
                  value={customEndDate}
                  onChange={(e) => setCustomEndDate(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                />
              </div>
            </div>
          </div>
        )}

        {/* Contador de resultados */}
        <div className="mt-4 flex items-center justify-between">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {filteredData.length} registros encontrados
          </span>
          <button
            onClick={() => {
              setSelectedLocation("all");
              setSelectedDateRange("week");
              setSearchQuery("");
              setCustomStartDate("");
              setCustomEndDate("");
              setShowCustomDate(false);
            }}
            className="text-sm text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300"
          >
            Limpiar filtros
          </button>
        </div>
      </div>

      {/* Tabla de resultados */}
      <div className="max-w-full overflow-x-auto">
        <Table>
          <TableHeader className="border-gray-100 dark:border-gray-800 border-y">
            <TableRow>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                Fecha y Hora
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                Ubicación
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                PM2.5
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                PM10
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                NO₂
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                Índice AQI
              </TableCell>
              <TableCell isHeader className="py-3 font-medium text-gray-500 text-start text-theme-xs">
                Estado
              </TableCell>
            </TableRow>
          </TableHeader>

          <TableBody className="divide-y divide-gray-100 dark:divide-gray-800">
            {filteredData.map((record) => {
              const aqiStatus = getAqiStatus(record.aqi);
              const aqiColor = getAqiColor(record.aqi);
              
              return (
                <TableRow key={record.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <TableCell className="py-3">
                    <div>
                      <p className="font-medium text-gray-800 text-theme-sm dark:text-white/90">
                        {record.timestamp.split(' ')[0]}
                      </p>
                      <span className="text-gray-500 text-theme-xs dark:text-gray-400">
                        {record.timestamp.split(' ')[1]}
                      </span>
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <div>
                      <p className="font-medium text-gray-800 text-theme-sm dark:text-white/90">
                        {record.location}
                      </p>
                      <span className="text-gray-500 text-theme-xs dark:text-gray-400">
                        {record.zone}
                      </span>
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <div className={`font-semibold ${record.pm25 > 35 ? 'text-red-600 dark:text-red-400' : 'text-gray-700 dark:text-gray-300'}`}>
                      {record.pm25.toFixed(1)} μg/m³
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <div className={`font-semibold ${record.pm10 > 50 ? 'text-red-600 dark:text-red-400' : 'text-gray-700 dark:text-gray-300'}`}>
                      {record.pm10.toFixed(1)} μg/m³
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <div className={`font-semibold ${record.no2 > 40 ? 'text-red-600 dark:text-red-400' : 'text-gray-700 dark:text-gray-300'}`}>
                      {record.no2.toFixed(1)} μg/m³
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-gray-700">
                        <div 
                          className={`h-full rounded-full ${
                            record.aqi <= 50 ? "bg-green-500" :
                            record.aqi <= 100 ? "bg-yellow-500" :
                            record.aqi <= 150 ? "bg-orange-500" :
                            record.aqi <= 200 ? "bg-red-500" : "bg-purple-500"
                          }`}
                          style={{ width: `${Math.min(100, (record.aqi / 200) * 100)}%` }}
                        />
                      </div>
                      <span className="font-bold text-gray-800 dark:text-white/90">
                        {record.aqi}
                      </span>
                    </div>
                  </TableCell>
                  
                  <TableCell className="py-3">
                    <Badge size="sm" color={aqiColor}>
                      {aqiStatus}
                    </Badge>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* Leyenda AQI */}
      <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-800">
        <h4 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">
          Leyenda del Índice de Calidad del Aire (AQI):
        </h4>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
          <div className="flex items-center gap-2 p-2 bg-green-50 rounded-lg dark:bg-green-900/20">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-xs text-gray-700 dark:text-gray-300">0-50: Buena</span>
          </div>
          <div className="flex items-center gap-2 p-2 bg-yellow-50 rounded-lg dark:bg-yellow-900/20">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-xs text-gray-700 dark:text-gray-300">51-100: Moderada</span>
          </div>
          <div className="flex items-center gap-2 p-2 bg-orange-50 rounded-lg dark:bg-orange-900/20">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="text-xs text-gray-700 dark:text-gray-300">101-150: Dañina</span>
          </div>
          <div className="flex items-center gap-2 p-2 bg-red-50 rounded-lg dark:bg-red-900/20">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-xs text-gray-700 dark:text-gray-300">151-200: Muy Dañina</span>
          </div>
          <div className="flex items-center gap-2 p-2 bg-purple-50 rounded-lg dark:bg-purple-900/20">
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
            <span className="text-xs text-gray-700 dark:text-gray-300">201+: Peligrosa</span>
          </div>
        </div>
      </div>
    </div>
  );
}