import { useState } from "react";
import api from "../services/api";

import HostCard from "../components/HostCard";
import FindingsTable from "../components/FindingsTable";
import AnalysisCard from "../components/AnalysisCard";
import StatsCards from "../components/StatsCards";
import HttpInfoCard from "../components/HttpInfoCard";

function Dashboard() {
  const [target, setTarget] = useState("");
  const [results, setResults] = useState([]);

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState("");

  const [startPort, setStartPort] = useState(1);
  const [endPort, setEndPort] = useState(1024);

  async function handleScan() {
    try {
      setLoading(true);

      setResults([]);

      const targets = target
        .split("\n")
        .map((t) => t.trim())
        .filter(Boolean);

      let tempResults = [];

      for (let i = 0; i < targets.length; i++) {
        setProgress(`Scanning ${i + 1} / ${targets.length} : ${targets[i]}`);

        const response = await api.post("/scan", {
          target: targets[i],
          start_port: startPort,
          end_port: endPort,
        });

        tempResults.push(response.data);

        setResults([...tempResults]);
      }

      setProgress("Scan Completed");
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

      <div className="flex flex-col gap-4">

        <textarea
          rows={3}
          placeholder={`Enter one target per line
          For Example=google.com
          192.168.x.x`}
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          className="w-[650px] rounded-lg bg-gray-800 border border-gray-700 px-4 py-3"
        />

        <div className="flex gap-4">

          <input
            type="number"
            value={startPort}
            onChange={(e) => setStartPort(Number(e.target.value))}
            className="w-40 rounded-lg bg-gray-800 border border-gray-700 px-4 py-3"
          />

          <input
            type="number"
            value={endPort}
            onChange={(e) => setEndPort(Number(e.target.value))}
            className="w-40 rounded-lg bg-gray-800 border border-gray-700 px-4 py-3"
          />

          <button
            onClick={handleScan}
            disabled={loading}
            className={`rounded-lg px-6 py-3 font-semibold ${
              loading
                ? "bg-gray-600 cursor-not-allowed"
                : "bg-cyan-500 hover:bg-cyan-400 text-black"
            }`}
          >
            {loading ? "Scanning..." : "Scan"}
          </button>

        </div>

        {loading && (
          <div className="flex items-center gap-3">

            <div className="h-5 w-5 animate-spin rounded-full border-4 border-cyan-400 border-t-transparent"></div>

            <p>{progress}</p>

          </div>
        )}

      </div>

      {results.map((result, index) => (
        <div key={index} className="mt-10 space-y-6">

          <h2 className="text-2xl font-bold text-cyan-400">
            {result.target}
          </h2>

          <StatsCards result={result} />

          <HostCard host={result.host} />

          <FindingsTable findings={result.findings} />

          <HttpInfoCard findings={result.findings} />

          <AnalysisCard analysis={result.analysis} />

        </div>
      ))}

    </div>
  );
}

export default Dashboard;