import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Station } from '../types/api.types';

// Importación necesaria para los iconos de Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';

// Fix para los iconos de Leaflet en React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetina,
  iconUrl: icon,
  shadowUrl: iconShadow,
});

// Iconos según el estado de la estación
const getMarkerIcon = (status: string) => {
  let iconColor = '#22c55e'; // green por defecto (active)
  
  if (status === 'inactive') {
    iconColor = '#ef4444'; // red
  } else if (status === 'maintenance') {
    iconColor = '#f59e0b'; // orange
  }

  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${iconColor}; 
        width: 28px; 
        height: 28px; 
        border-radius: 50%; 
        border: 3px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <div style="
          width: 12px;
          height: 12px;
          background: white;
          border-radius: 50%;
        "></div>
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
};

interface CaliMapComponentProps {
  stations: Station[];
}

export default function CaliMapComponent({ stations }: CaliMapComponentProps) {
  // Centro de Cali, Colombia
  const caliCoordinates: [number, number] = [3.4516, -76.532];

  return (
    <MapContainer
      center={caliCoordinates}
      zoom={12}
      minZoom={10}
      maxZoom={18}
      style={{
        height: '100%',
        width: '100%',
        borderRadius: '8px',
        zIndex: 1,
      }}
      scrollWheelZoom={true}
      className="leaflet-container"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={19}
      />

      {/* Marcadores dinámicos desde el backend */}
      {stations.map((station) => {
        const [lon, lat] = station.location.coordinates;
        
        return (
          <Marker
            key={station.id}
            position={[lat, lon]}
            icon={getMarkerIcon(station.status)}
          >
            <Popup>
              <div className="p-2 min-w-[200px]">
                <h3 className="font-bold text-base mb-1">{station.name}</h3>
                <p className="text-sm text-gray-600 mb-1">{station.address}</p>
                <p className="text-xs text-gray-500 mb-2">
                  {station.institution_name}
                </p>
                
                <div className="flex items-center gap-2 mb-2">
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      station.status === 'active'
                        ? 'bg-green-100 text-green-800'
                        : station.status === 'maintenance'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {station.status}
                  </span>
                </div>

                <div className="text-xs text-gray-600">
                  <div className="flex justify-between">
                    <span>Sensores:</span>
                    <span className="font-semibold">{station.devices_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Alertas:</span>
                    <span className="font-semibold">{station.alerts_count}</span>
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}