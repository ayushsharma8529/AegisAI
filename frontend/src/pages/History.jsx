import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
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
              <th className="p-4 text-left">Target</th>
              <th className="p-4 text-left">Status</th>
              <th className="p-4 text-left">Date</th>
              <th className="p-4 text-center">Action</th>
              <th className="p-3">ID</th>
            </tr>

          </thead>

          <tbody>
  {history.map((scan) => (
    <tr
      key={scan.id}
      className="border-t border-gray-700 hover:bg-gray-800"
    >
      <td className="p-3">{scan.id}</td>

      <td className="p-3">{scan.target}</td>

      <td className="p-3">{scan.status}</td>

      <td className="p-3">{scan.created_at}</td>

      <td className="p-3 text-center">
        <Link
          to={`/history/${scan.id}`}
          className="bg-cyan-500 px-3 py-1 rounded hover:bg-cyan-600"
        >
          View Report
        </Link>
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