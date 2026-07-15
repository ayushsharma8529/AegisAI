import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../services/api";

import HostCard from "../components/HostCard";
import FindingsTable from "../components/FindingsTable";
import AnalysisCard from "../components/AnalysisCard";
import StatsCards from "../components/StatsCards";

function ScanDetails() {
  const { id } = useParams();

  console.log("ScanDetails mounted");
  console.log("ID =", id);

  const [result, setResult] = useState(null);

  useEffect(() => {
    async function loadScan() {
      console.log("Calling API...");

      try {
        const response = await api.get(`/history/${id}`);

        console.log("API Response:", response.data);

        setResult(response.data);
      } catch (error) {
        console.error("API ERROR:", error);
      }
    }

    loadScan();
  }, [id]);

  if (!result) {
    return (
      <div className="min-h-screen bg-gray-950 text-white p-8">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        Scan Report
      </h1>

      <div className="space-y-6">
        <StatsCards result={result} />
        <HostCard host={result.host} />
        <FindingsTable findings={result.findings} />
        <AnalysisCard analysis={result.analysis} />
      </div>

    </div>
  );
}  
    
export default ScanDetails;