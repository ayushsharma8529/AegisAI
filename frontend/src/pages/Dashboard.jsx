import { useState } from "react";
import api from "../services/api";
import HostCard from "../components/HostCard";
import FindingsTable from "../components/FindingsTable";
import AnalysisCard from "../components/AnalysisCard";

function Dashboard() {
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);

  async function handleScan() {
    try {
      const response = await api.post("/scan", {
        target: target,
        start_port: 445,
        end_port: 445,
      });

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Scan failed");
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        🛡️ AegisAI Dashboard
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
          className="rounded-lg bg-cyan-500 px-6 py-3 font-semibold text-black hover:bg-cyan-400 transition"
        >
          Scan
        </button>

      </div>

      {result && (
        <div className="mt-10 space-y-6">

          <HostCard host={result.host} />

          <FindingsTable findings={result.findings} />

          <AnalysisCard analysis={result.analysis} />

        </div>
      )}

    </div>
  );
}

export default Dashboard;