import { useEffect, useState } from "react";
import api from "../services/api";

function History() {
  const [history, setHistory] = useState([]);

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

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        📜 Scan History
      </h1>

      <div className="overflow-x-auto rounded-xl border border-gray-700">

        <table className="w-full">

          <thead className="bg-gray-800">

            <tr>
              <th className="p-3">ID</th>
              <th className="p-4 text-left">Target</th>
              <th className="p-4 text-left">Status</th>
              <th className="p-4 text-left">Date</th>
              <th className="p-4 text-center">Action</th>
            </tr>

          </thead>

          <tbody>
            {history.map((scan) => (
              <tr
                key={scan.id}
                className="border-t border-gray-700 hover:bg-gray-800"
              >
                <td className="p-3 text-center">{scan.id}</td>

                <td className="p-3 font-semibold text-gray-200">{scan.target}</td>

                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${
                    scan.status === "completed" || scan.status === "online" 
                      ? "bg-green-900/50 text-green-400 border border-green-700" 
                      : "bg-yellow-900/50 text-yellow-400 border border-yellow-700"
                  }`}>
                    {scan.status}
                  </span>
                </td>

                <td className="p-3 text-gray-400">{scan.created_at}</td>

                <td className="p-3 text-center">
                  <button
                    onClick={() =>
                      window.open(
                        `http://127.0.0.1:8000/report/${scan.id}`,
                        "_blank"
                      )
                    }
                    className="bg-cyan-500 hover:bg-cyan-600 text-gray-950 font-bold px-4 py-1.5 rounded-lg transition duration-200"
                  >
                    View Report
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>

    </div>
  );
}

export default History;