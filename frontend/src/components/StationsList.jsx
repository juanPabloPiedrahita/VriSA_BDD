import React, { useState, useEffect } from 'react';
import { stationsService } from '../services/stations.service';

const StationsList = () => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStations();
  }, []);

  const fetchStations = async () => {
    try {
      const data = await stationsService.getAll();
      setStations(data.results || data);
    } catch (err) {
      setError('Error al cargar estaciones');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Cargando...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Estaciones de Monitoreo</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stations.map((station) => (
          <div key={station.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-2">{station.name}</h3>
            <p className="text-gray-600 mb-2">{station.address}</p>
            <span className={`px-2 py-1 rounded text-sm ${
              station.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
            }`}>
              {station.status}
            </span>
            <p className="text-sm text-gray-500 mt-2">
              {station.institution_name}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StationsList;