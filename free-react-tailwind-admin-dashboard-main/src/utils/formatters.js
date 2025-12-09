// Funciones de formato
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO');
};

export const formatDateTime = (date) => {
  return new Date(date).toLocaleString('es-CO');
};

export const formatNumber = (num, decimals = 2) => {
  return Number(num).toFixed(decimals);
};
