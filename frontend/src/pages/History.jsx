import { useEffect, useState } from "react";
import api from "../services/api";

function History() {
  const [history, setHistory] = useState([]);
  // 🔥 Step 1: Search state
  const [search, setSearch] = useState("");

  // Base URL dynamically fetched from the axios instance configuration
  const API_BASE_URL = api.defaults.baseURL;

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await api.get("/history");
        setHistory(response.data);
      } catch (error) {
        console.error(error);
      }
    }

    loadHistory();
  }, []);

  // 🔥 Step 5 (Delete): Handle delete click with instant UI update
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this scan?")) {
      return;
    }

    try {
      await api.delete(`/history/${id}`);
      // UI state filter out karke bina hard-refresh ke updates apply ho jayenge
      setHistory(history.filter((scan) => scan.id !== id));
    } catch (err) {
      console.error("Error deleting scan:", err);
    }
  };

  // 🔥 Step 5: Better Status Colors Helper
  const getStatusColor = (status) => {
    switch (status) {
      case "completed":
      case "online":
        return "bg-green-900/50 text-green-400 border border-green-700/50";
      case "failed":
        return "bg-red-900/50 text-red-400 border border-red-700/50";
      default:
        return "bg-yellow-900/50 text-yellow-400 border border-yellow-700/50";
    }
  };

  // 🔥 Step 2: Filter logic
  const filteredHistory = history.filter((scan) =>
    scan.target.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        📜 Scan History
      </h1>

      {/* 🔥 Step 1: Search Input UI */}
      <input
        type="text"
        placeholder="Search target..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-6 w-80 rounded-lg bg-gray-800 border border-gray-700 px-4 py-2 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition duration-150"
      />

      {/* 🔥 Step 4: Empty State (Handles empty history OR zero search matches) */}
      {filteredHistory.length === 0 ? (
        <div className="text-center py-16 text-gray-500 bg-gray-900/20 rounded-xl border border-gray-800">
          {history.length === 0 ? "No scans available." : "No matching targets found."}
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-700">
          <table className="w-full">
            <thead className="bg-gray-800">
              <tr>
                <th className="p-3">ID</th>
                <th className="p-4 text-left">Target</th>
                <th className="p-4 text-left">Status</th>
                <th className="p-4 text-left">Date</th>
                {/* Cleaned Header for Action Column */}
                <th className="p-4 text-center">Actions</th>
              </tr>
            </thead>

            <tbody>
              {/* 🔥 Step 2: Render Filtered Scans */}
              {filteredHistory.map((scan) => (
                <tr
                  key={scan.id}
                  className="border-t border-gray-700 hover:bg-gray-800 transition duration-150"
                >
                  <td className="p-3 text-center text-gray-400 font-mono">{scan.id}</td>

                  <td className="p-3 font-semibold text-gray-200">{scan.target}</td>

                  <td className="p-3">
                    {/* 🔥 Step 5: Beautiful Dynamic Badge */}
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(scan.status)}`}>
                      {scan.status}
                    </span>
                  </td>

                  {/* 🔥 Step 3: Professional Readable Date Format */}
                  <td className="p-3 text-gray-400">
                    {new Date(scan.created_at).toLocaleString()}
                  </td>

                  <td className="p-3 text-center flex items-center justify-center gap-2">
                    {/* View Report Button - Environment Dynamic URL */}
                    <button
                      onClick={() =>
                        window.open(
                          `${API_BASE_URL}/report/${scan.id}`,
                          "_blank"
                        )
                      }
                      className="bg-cyan-500 hover:bg-cyan-600 text-gray-950 font-bold px-4 py-1.5 rounded-lg transition duration-200 text-sm"
                    >
                      View Report
                    </button>

                    {/* 🔥 Step 4: Delete Button */}
                    <button
                      onClick={() => handleDelete(scan.id)}
                      className="bg-red-600 hover:bg-red-700 text-white font-bold px-4 py-1.5 rounded-lg transition duration-200 text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;