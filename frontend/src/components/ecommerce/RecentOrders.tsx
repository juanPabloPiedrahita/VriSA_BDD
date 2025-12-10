// ContaminationIndex.tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../ui/table";
import Badge from "../ui/badge/Badge";

// Define the TypeScript interface for contamination data
interface Contaminant {
  id: number;
  name: string;
  scientificName: string;
  currentLevel: number;
  unit: string;
  safeLimit: number;
  status: "Bajo" | "Moderado" | "Alto" | "Muy Alto" | "Peligroso";
  trend: "up" | "down" | "stable";
  source: string;
}

// Contamination data for Cali, Colombia based on current reports
const contaminationData: Contaminant[] = [
  {
    id: 1,
    name: "PM2.5",
    scientificName: "Partículas finas",
    currentLevel: 28.5,
    unit: "μg/m³",
    safeLimit: 25,
    status: "Moderado",
    trend: "up",
    source: "Tráfico vehicular, incendios"
  },
  {
    id: 2,
    name: "PM10",
    scientificName: "Partículas respirables",
    currentLevel: 42.3,
    unit: "μg/m³",
    safeLimit: 50,
    status: "Bajo",
    trend: "stable",
    source: "Polvo, construcción"
  },
  {
    id: 3,
    name: "NO₂",
    scientificName: "Dióxido de nitrógeno",
    currentLevel: 38.7,
    unit: "μg/m³",
    safeLimit: 40,
    status: "Bajo",
    trend: "down",
    source: "Vehículos diesel"
  },
  {
    id: 4,
    name: "O₃",
    scientificName: "Ozono troposférico",
    currentLevel: 65.2,
    unit: "μg/m³",
    safeLimit: 100,
    status: "Moderado",
    trend: "up",
    source: "Reacciones químicas"
  },
  {
    id: 5,
    name: "SO₂",
    scientificName: "Dióxido de azufre",
    currentLevel: 12.4,
    unit: "μg/m³",
    safeLimit: 20,
    status: "Bajo",
    trend: "stable",
    source: "Industria, combustibles"
  },
  {
    id: 6,
    name: "CO",
    scientificName: "Monóxido de carbono",
    currentLevel: 1.8,
    unit: "mg/m³",
    safeLimit: 4,
    status: "Bajo",
    trend: "down",
    source: "Combustión incompleta"
  },
];

// Function to get color based on status
const getStatusColor = (status: Contaminant["status"]) => {
  switch (status) {
    case "Bajo":
      return "success";
    case "Moderado":
      return "warning";
    case "Alto":
      return "error";
    case "Muy Alto":
      return "error";
    case "Peligroso":
      return "error";
    default:
      return "warning";
  }
};

// Function to get trend icon
const getTrendIcon = (trend: Contaminant["trend"]) => {
  switch (trend) {
    case "up":
      return (
        <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      );
    case "down":
      return (
        <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      );
    case "stable":
      return (
        <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
        </svg>
      );
    default:
      return null;
  }
};

export default function ContaminationIndex() {
  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
      <div className="flex flex-col gap-2 mb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Índice de Contaminantes - Cali
          </h3>
          <p className="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
            Calidad del aire y niveles de contaminación actuales
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-theme-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200">
            <svg
              className="stroke-current fill-white dark:fill-gray-800"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2.29004 5.90393H17.7067"
                stroke=""
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M17.7075 14.0961H2.29085"
                stroke=""
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12.0826 3.33331C13.5024 3.33331 14.6534 4.48431 14.6534 5.90414C14.6534 7.32398 13.5024 8.47498 12.0826 8.47498C10.6627 8.47498 9.51172 7.32398 9.51172 5.90415C9.51172 4.48432 10.6627 3.33331 12.0826 3.33331Z"
                fill=""
                stroke=""
                strokeWidth="1.5"
              />
              <path
                d="M7.91745 11.525C6.49762 11.525 5.34662 12.676 5.34662 14.0959C5.34661 15.5157 6.49762 16.6667 7.91745 16.6667C9.33728 16.6667 10.4883 15.5157 10.4883 14.0959C10.4883 12.676 9.33728 11.525 7.91745 11.525Z"
                fill=""
                stroke=""
                strokeWidth="1.5"
              />
            </svg>
            Filtrar
          </button>
          <button className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-theme-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200">
            Ver histórico
          </button>
        </div>
      </div>
      
      <div className="max-w-full overflow-x-auto">
        <Table>
          {/* Table Header */}
          <TableHeader className="border-gray-100 dark:border-gray-800 border-y">
            <TableRow>
              <TableCell
                isHeader
                className="py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
              >
                Contaminante
              </TableCell>
              <TableCell
                isHeader
                className="py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
              >
                Nivel Actual
              </TableCell>
              <TableCell
                isHeader
                className="py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
              >
                Límite Seguro
              </TableCell>
              <TableCell
                isHeader
                className="py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
              >
                Tendencia
              </TableCell>
              <TableCell
                isHeader
                className="py-3 font-medium text-gray-500 text-start text-theme-xs dark:text-gray-400"
              >
                Estado
              </TableCell>
            </TableRow>
          </TableHeader>

          {/* Table Body */}
          <TableBody className="divide-y divide-gray-100 dark:divide-gray-800">
            {contaminationData.map((contaminant) => (
              <TableRow key={contaminant.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                <TableCell className="py-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center h-10 w-10 rounded-md bg-gray-100 dark:bg-gray-800">
                      <span className="font-semibold text-gray-700 dark:text-gray-300">
                        {contaminant.name}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 text-theme-sm dark:text-white/90">
                        {contaminant.scientificName}
                      </p>
                      <span className="text-gray-500 text-theme-xs dark:text-gray-400">
                        {contaminant.source}
                      </span>
                    </div>
                  </div>
                </TableCell>
                
                <TableCell className="py-3">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-800 text-theme-sm dark:text-white/90">
                      {contaminant.currentLevel.toFixed(1)} {contaminant.unit}
                    </span>
                    {getTrendIcon(contaminant.trend)}
                  </div>
                </TableCell>
                
                <TableCell className="py-3">
                  <span className="text-gray-500 text-theme-sm dark:text-gray-400">
                    {contaminant.safeLimit} {contaminant.unit}
                  </span>
                </TableCell>
                
                <TableCell className="py-3">
                  <div className="flex items-center">
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-gray-700">
                      <div 
                        className={`h-full rounded-full ${
                          contaminant.currentLevel > contaminant.safeLimit * 1.5 
                            ? "bg-red-500" 
                            : contaminant.currentLevel > contaminant.safeLimit 
                            ? "bg-yellow-500" 
                            : "bg-green-500"
                        }`}
                        style={{ 
                          width: `${Math.min(100, (contaminant.currentLevel / (contaminant.safeLimit * 1.5)) * 100)}%` 
                        }}
                      />
                    </div>
                  </div>
                </TableCell>
                
                <TableCell className="py-3">
                  <div className="flex items-center gap-2">
                    <Badge
                      size="sm"
                      color={getStatusColor(contaminant.status)}
                    >
                      {contaminant.status}
                    </Badge>
                    <span className="text-gray-500 text-theme-xs dark:text-gray-400">
                      {contaminant.currentLevel > contaminant.safeLimit ? "⚠️" : "✅"}
                    </span>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      
      {/* Legend Section */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
        <div className="flex flex-wrap items-center gap-4 text-theme-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Bajo: Dentro de límites seguros</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span>Moderado: Ligeramente elevado</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>Alto/Muy Alto: Supera límites seguros</span>
          </div>
        </div>
      </div>
    </div>
  );
}