// CaliMapComponent.tsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Importación necesaria para los iconos de Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';

// Coordenadas de Cali, Colombia
const caliCoordinates: [number, number] = [3.4516, -76.5320];

// Configuración del icono personalizado
const customIcon = new L.Icon({
  iconUrl: icon,
  iconRetinaUrl: iconRetina,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

// Fix para los iconos de Leaflet en React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetina,
  iconUrl: icon,
  shadowUrl: iconShadow,
});

// Coordenadas para diferentes zonas de Cali
const caliLocations = [
  { 
    name: 'Centro de Cali', 
    coordinates: [3.4516, -76.5320] as [number, number],
    description: 'Zona comercial y administrativa'
  },
  { 
    name: 'Norte de Cali', 
    coordinates: [3.4800, -76.5200] as [number, number],
    description: 'Zona residencial y empresarial'
  },
  { 
    name: 'Sur de Cali', 
    coordinates: [3.4200, -76.5450] as [number, number],
    description: 'Zona residencial y comercial'
  },
  { 
    name: 'Oeste de Cali', 
    coordinates: [3.4550, -76.5600] as [number, number],
    description: 'Zona universitaria y cultural'
  },
  { 
    name: 'Este de Cali', 
    coordinates: [3.4500, -76.4950] as [number, number],
    description: 'Zona industrial y residencial'
  }
];

export default function CaliMapComponent() {
  return (
    <MapContainer
      center={caliCoordinates}
      zoom={11} // Zoom más abierto para ver más área
      minZoom={10}
      maxZoom={16}
      style={{ 
        height: '100%', 
        width: '100%', 
        borderRadius: '8px',
        zIndex: 1 
      }}
      scrollWheelZoom={true}
      className="leaflet-container"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={19}
        tileSize={512}
        zoomOffset={-1}
      />
      
      {/* Marcadores para diferentes zonas de Cali */}
      {caliLocations.map((location, index) => (
        <Marker 
          key={index} 
          position={location.coordinates} 
          icon={customIcon}
        >
          <Popup>
            <div className="p-1">
              <strong className="text-sm font-semibold">{location.name}</strong><br />
              <span className="text-xs text-gray-600">{location.description}</span>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}