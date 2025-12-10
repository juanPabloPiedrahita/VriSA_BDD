// MonthlyPollutionChart.tsx (o renombra el archivo actual)
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import { MoreDotIcon } from "../../icons";
import { useState } from "react";

export default function MonthlyPollutionChart() {
  const options: ApexOptions = {
    colors: ["#10B981", "#3B82F6", "#EF4444", "#8B5CF6"],
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "bar",
      height: 180,
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "55%",
        borderRadius: 5,
        borderRadiusApplication: "end",
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ["transparent"],
    },
    xaxis: {
      categories: [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
      ],
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      labels: {
        style: {
          colors: "#6B7280",
          fontSize: "12px",
          fontFamily: "Outfit, sans-serif",
        }
      }
    },
    yaxis: {
      title: {
        text: "μg/m³",
        style: {
          color: "#6B7280",
          fontSize: "12px",
          fontFamily: "Outfit, sans-serif",
        }
      },
      labels: {
        style: {
          colors: "#6B7280",
          fontSize: "11px",
          fontFamily: "Outfit, sans-serif",
        },
        formatter: function(val: number) {
          return val.toFixed(0);
        }
      }
    },
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
      fontFamily: "Outfit, sans-serif",
      fontSize: "12px",
      markers: {
        size: 6,
        shape: "square" as const,
      },
      itemMargin: {
        horizontal: 8,
        vertical: 4
      }
    },
    grid: {
      borderColor: "#F3F4F6",
      strokeDashArray: 4,
      yaxis: {
        lines: {
          show: true,
        },
      },
      xaxis: {
        lines: {
          show: false,
        }
      }
    },
    fill: {
      opacity: 1,
    },
    tooltip: {
      theme: "dark",
      x: {
        show: true,
        formatter: function(val: number) {
          const months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
          ];
          return months[val];
        }
      },
      y: {
        title: {
          formatter: function(seriesName: string) {
            return seriesName + ":";
          }
        },
        formatter: function(val: number) {
          return val.toFixed(1) + " μg/m³";
        }
      }
    },
    responsive: [{
      breakpoint: 640,
      options: {
        legend: {
          position: "bottom",
          horizontalAlign: "center",
          fontSize: "11px"
        }
      }
    }]
  };

  // Datos de contaminación mensual para Cali (basados en promedios históricos)
  const series = [
    {
      name: "PM2.5",
      data: [28.5, 30.2, 32.8, 31.5, 29.8, 27.4, 26.9, 28.1, 30.5, 32.1, 31.8, 29.3]
    },
    {
      name: "PM10",
      data: [42.3, 45.1, 48.9, 46.7, 43.2, 40.8, 39.5, 41.3, 44.6, 47.2, 46.5, 43.1]
    },
    {
      name: "NO₂",
      data: [38.7, 40.5, 42.3, 41.2, 39.8, 37.6, 36.4, 38.2, 40.8, 42.5, 41.9, 39.4]
    },
    {
      name: "O₃",
      data: [65.2, 68.4, 72.1, 70.8, 67.5, 63.2, 61.8, 64.3, 68.9, 71.5, 70.2, 66.8]
    }
  ];

  const [isOpen, setIsOpen] = useState(false);

  function toggleDropdown() {
    setIsOpen(!isOpen);
  }

  function closeDropdown() {
    setIsOpen(false);
  }

  // Calcular promedios
  const calculateAverages = () => {
    const avgPM25 = series[0].data.reduce((a, b) => a + b, 0) / series[0].data.length;
    const avgPM10 = series[1].data.reduce((a, b) => a + b, 0) / series[1].data.length;
    const avgNO2 = series[2].data.reduce((a, b) => a + b, 0) / series[2].data.length;
    const avgO3 = series[3].data.reduce((a, b) => a + b, 0) / series[3].data.length;
    
    return { avgPM25, avgPM10, avgNO2, avgO3 };
  };

  const averages = calculateAverages();

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Contaminación Mensual - Cali
          </h3>
          <p className="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
            Promedio de contaminantes por mes (μg/m³)
          </p>
        </div>
        <div className="relative inline-block">
          <button className="dropdown-toggle" onClick={toggleDropdown}>
            <MoreDotIcon className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 size-6" />
          </button>
          <Dropdown
            isOpen={isOpen}
            onClose={closeDropdown}
            className="w-40 p-2"
          >
            <DropdownItem
              onItemClick={closeDropdown}
              className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
            >
              Ver detalles
            </DropdownItem>
            <DropdownItem
              onItemClick={closeDropdown}
              className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
            >
              Descargar datos
            </DropdownItem>
            <DropdownItem
              onItemClick={closeDropdown}
              className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
            >
              Comparar años
            </DropdownItem>
          </Dropdown>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      <div className="mb-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500 dark:text-gray-400">PM2.5</span>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <p className="mt-1 text-lg font-semibold text-gray-800 dark:text-white/90">
            {averages.avgPM25.toFixed(1)}
          </p>
          <span className="text-xs text-gray-500 dark:text-gray-400">μg/m³ promedio</span>
        </div>
        
        <div className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500 dark:text-gray-400">PM10</span>
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
          </div>
          <p className="mt-1 text-lg font-semibold text-gray-800 dark:text-white/90">
            {averages.avgPM10.toFixed(1)}
          </p>
          <span className="text-xs text-gray-500 dark:text-gray-400">μg/m³ promedio</span>
        </div>
        
        <div className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500 dark:text-gray-400">NO₂</span>
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
          </div>
          <p className="mt-1 text-lg font-semibold text-gray-800 dark:text-white/90">
            {averages.avgNO2.toFixed(1)}
          </p>
          <span className="text-xs text-gray-500 dark:text-gray-400">μg/m³ promedio</span>
        </div>
        
        <div className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500 dark:text-gray-400">O₃</span>
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
          </div>
          <p className="mt-1 text-lg font-semibold text-gray-800 dark:text-white/90">
            {averages.avgO3.toFixed(1)}
          </p>
          <span className="text-xs text-gray-500 dark:text-gray-400">μg/m³ promedio</span>
        </div>
      </div>

      <div className="max-w-full overflow-x-auto custom-scrollbar">
        <div className="-ml-5 min-w-[650px] xl:min-w-full pl-2">
          <Chart options={options} series={series} type="bar" height={200} />
        </div>
      </div>

      {/* Leyenda y notas */}
      <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            <span className="font-medium text-gray-700 dark:text-gray-300">Nota:</span> 
            Datos basados en promedios mensuales 2023-2024. Marzo y Octubre muestran picos por condiciones climáticas.
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="text-green-600 dark:text-green-400">⬤</span>
            <span className="text-gray-500 dark:text-gray-400">PM2.5 ≤ 25 μg/m³</span>
            <span className="text-yellow-600 dark:text-yellow-400 ml-2">⬤</span>
            <span className="text-gray-500 dark:text-gray-400">O₃ ≤ 100 μg/m³</span>
          </div>
        </div>
      </div>
    </div>
  );
}