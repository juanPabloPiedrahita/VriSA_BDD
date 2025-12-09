// Contexto de estaciones
import React, { createContext, useState, useContext } from 'react';

const StationsContext = createContext();

export const StationsProvider = ({ children }) => {
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);

  return (
    <StationsContext.Provider value={{ stations, setStations, selectedStation, setSelectedStation }}>
      {children}
    </StationsContext.Provider>
  );
};

export const useStations = () => useContext(StationsContext);
