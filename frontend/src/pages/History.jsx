import { useEffect, useState } from "react";
import api from "../services/api";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function loadHistory() {
      const response = await api.get("/history");
      setHistory(response.data);
    }

    loadHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        Scan History
      </h1>

      <table className="w-full border border-gray-700">
        <thead className="bg-gray-800">
          <tr>
            <th className="p-3">Target</th>
            <th className="p-3">Status</th>
            <th className="p-3">Date</th>
          </tr>
        </thead>

        <tbody>
          {history.map((scan) => (
            <tr
              key={scan.id}
              className="border-t border-gray-700 hover:bg-gray-800"
            >
              <td className="p-3">{scan.target}</td>
              <td className="p-3">{scan.status}</td>
              <td className="p-3">{scan.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default History;