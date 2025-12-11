import { Station } from "../../types/api.types";
import CaliMapComponent from "../CaliMapComponent"; // Ajusta la ruta según tu estructura

interface DemographicCardProps {
  stations: Station[];
}

export default function DemographicCard({ stations }: DemographicCardProps) {
  return (
    <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div className="border-b border-stroke px-7 py-4 dark:border-strokedark">
        <h3 className="font-medium text-black dark:text-white">
          Mapa de Estaciones - Cali
        </h3>
      </div>
      
      <div className="p-7">
        <div className="mb-4">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {stations.filter(s => s.status === 'active').length} estaciones activas
          </p>
        </div>
        
        {/* Mapa con altura fija */}
        <div style={{ height: '400px', width: '100%' }}>
          <CaliMapComponent stations={stations} />
        </div>

        {/* Leyenda */}
        <div className="mt-4 flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Activa</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <span>Mantenimiento</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>Inactiva</span>
          </div>
        </div>
      </div>
    </div>
  );
}