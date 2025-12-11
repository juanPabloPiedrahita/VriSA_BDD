import { useEffect, useState } from "react";
import { stationsService } from "../../services/stations.service";
import { alertsService } from "../../services/alerts.service";
import { Station, Alert } from "../../types/api.types";
import EcommerceMetrics from "../../components/ecommerce/EcommerceMetrics";
import MonthlySalesChart from "../../components/ecommerce/MonthlySalesChart";
import RecentOrders from "../../components/ecommerce/RecentOrders";
import DemographicCard from "../../components/ecommerce/DemographicCard";
import PageMeta from "../../components/common/PageMeta";

export default function Home() {
  const [stations, setStations] = useState<Station[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    activeStations: 0,
    totalSensors: 0,
    activeAlerts: 0,
    attendedAlerts: 0,
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Cargar estaciones
      const stationsData = await stationsService.getAll({ page_size: 100 });
      setStations(stationsData.results);

      // Cargar alertas
      const alertsData = await alertsService.getAll({ page_size: 100 });
      setAlerts(alertsData.results);

      // Calcular estadísticas
      const activeStations = stationsData.results.filter(
        (s) => s.status === "active"
      ).length;
      const totalSensors = stationsData.results.reduce(
        (sum, s) => sum + s.devices_count,
        0
      );
      const activeAlerts = alertsData.results.filter((a) => !a.attended).length;
      const attendedAlerts = alertsData.results.filter((a) => a.attended).length;

      setStats({
        activeStations,
        totalSensors,
        activeAlerts,
        attendedAlerts,
      });
    } catch (error) {
      console.error("Error cargando datos del dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Cargando datos...</div>
      </div>
    );
  }

  return (
    <>
      <PageMeta
        title="Monitoreo VRISA"
        description="Panel de control para monitorear la calidad del aire en Cali."
      />
      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12 space-y-6 xl:col-span-7">
          {/* Pasar stats reales */}
          <EcommerceMetrics stats={stats} />
          
          {/* Pasar alertas reales */}
          <MonthlySalesChart alerts={alerts} />
        </div>
        
        <div className="col-span-12 xl:col-span-5">
          {/* Pasar estaciones reales */}
          <DemographicCard stations={stations} />
        </div>
        
        <div className="col-span-12 xl:col-span-7">
          {/* Pasar alertas reales */}
          <RecentOrders alerts={alerts} />
        </div>
      </div>
    </>
  );
}