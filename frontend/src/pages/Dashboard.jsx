import { useState } from "react";
import api from "../services/api";
import HostCard from "../components/HostCard";
import FindingsTable from "../components/FindingsTable";
import AnalysisCard from "../components/AnalysisCard";
import StatsCards from "../components/StatsCards";

function Dashboard() {
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);


    async function handleScan() {
  try {
    setLoading(true);

    const response = await api.post("/scan", {
      target,
      start_port: 445,
      end_port: 445,
    });

    setResult(response.data);
  } catch (error) {
    console.error(error);
    alert("Scan failed");
  } finally {
    setLoading(false);
  }
}

   
  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
         Dashboard
      </h1>

      <div className="flex gap-4 items-center flex-wrap">

        <input
          type="text"
          placeholder="Enter Target IP"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          className="w-96 rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500"
        />

       <button
       onClick={handleScan}
       disabled={loading}
       className={`rounded-lg px-6 py-3 font-semibold transition ${
       loading
      ? "bg-gray-600 cursor-not-allowed"
      : "bg-cyan-500 hover:bg-cyan-400 text-black"
       }`}
      >
      {loading ? "Scanning..." : "Scan"}
        </button>
          
      {loading && (
  <div className="mt-6 flex items-center gap-3 text-cyan-400">
    <div className="h-5 w-5 animate-spin rounded-full border-4 border-cyan-400 border-t-transparent"></div>
    <p>Scanning target...</p>
  </div>
)}
      </div>

      {result && (
        <div className="mt-10 space-y-6">

          <StatsCards result={result} />

          <HostCard host={result.host} />

          <FindingsTable findings={result.findings} />

          <AnalysisCard analysis={result.analysis} />

        </div>
      )}

    </div>
  );
}

export default Dashboard;