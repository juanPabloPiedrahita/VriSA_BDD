interface EcommerceMetricsProps {
  stats: {
    activeStations: number;
    totalSensors: number;
    activeAlerts: number;
    attendedAlerts: number;
  };
}

export default function EcommerceMetrics({ stats }: EcommerceMetricsProps) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
      {/* Estaciones Activas */}
      <div className="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg className="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22">
            {/* Icono de ubicación/estación */}
            <path d="M11 0C6.58 0 3 3.58 3 8c0 5.25 8 14 8 14s8-8.75 8-14c0-4.42-3.58-8-8-8zm0 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"/>
          </svg>
        </div>

        <div className="mt-4 flex items-end justify-between">
          <div>
            <h4 className="text-title-md font-bold text-black dark:text-white">
              {stats.activeStations}
            </h4>
            <span className="text-sm font-medium">Estaciones Activas</span>
          </div>
        </div>
      </div>

      {/* Sensores Totales */}
      <div className="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg className="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22">
            {/* Icono de sensor */}
            <circle cx="11" cy="11" r="8"/>
          </svg>
        </div>

        <div className="mt-4 flex items-end justify-between">
          <div>
            <h4 className="text-title-md font-bold text-black dark:text-white">
              {stats.totalSensors}
            </h4>
            <span className="text-sm font-medium">Sensores Instalados</span>
          </div>
        </div>
      </div>

      {/* Alertas Activas */}
      <div className="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg className="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22">
            <path d="M11 0L0 11h6v11h10V11h6L11 0z"/>
          </svg>
        </div>

        <div className="mt-4 flex items-end justify-between">
          <div>
            <h4 className="text-title-md font-bold text-black dark:text-white">
              {stats.activeAlerts}
            </h4>
            <span className="text-sm font-medium">Alertas Pendientes</span>
          </div>
        </div>
      </div>

      {/* Alertas Atendidas */}
      <div className="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg className="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
          </svg>
        </div>

        <div className="mt-4 flex items-end justify-between">
          <div>
            <h4 className="text-title-md font-bold text-black dark:text-white">
              {stats.attendedAlerts}
            </h4>
            <span className="text-sm font-medium">Alertas Resueltas</span>
          </div>
        </div>
      </div>
    </div>
  );
}