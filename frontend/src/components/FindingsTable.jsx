import React from 'react';

function FindingsTable({ findings }) {
  if (!findings || findings.length === 0) {
    return null;
  }

  const severityColor = {
    Critical: "bg-red-700",
    High: "bg-red-500",
    Medium: "bg-yellow-500 text-black",
    Low: "bg-green-500",
  };

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-lg">

      <h2 className="mb-6 text-2xl font-bold text-cyan-400">
        🔓 Open Ports & Security Findings
      </h2>

      <div className="overflow-x-auto">

        <table className="w-full border-collapse">

          <thead>
            <tr className="border-b border-gray-700 text-left text-gray-300">
              <th className="p-4">Port</th>
              <th className="p-4">Service</th>
              <th className="p-4">Severity</th>
              <th className="p-4">MITRE</th>
              <th className="p-4">CVE</th>
              <th className="p-4">Web Vulns</th>
              <th className="p-4">Recommendation</th>
            </tr>
          </thead>

          <tbody>
            {findings.map((item, index) => (
              <tr
                key={index}
                className="border-b border-gray-800 hover:bg-gray-800 transition"
              >
                <td className="p-4 font-semibold">{item.port}</td>

                <td className="p-4">{item.service}</td>

                <td className="p-4">
                  <span
                    className={`rounded-full px-3 py-1 text-sm font-bold text-white ${
                      severityColor[item.severity] || "bg-gray-600"
                    }`}
                  >
                    {item.severity}
                  </span>
                </td>

                <td className="p-4">
                  {item.mitre?.technique || "-"}
                </td>

                <td className="p-4">
                  {item.cves?.length > 0
                    ? item.cves[0].id
                    : "-"}
                </td>

                {/* Step 2: Added Web Vulns cell right after CVE */}
                <td className="p-4">
                  {item.web_vulnerabilities?.length ? (
                    <span className="rounded-full bg-red-600 px-3 py-1 text-sm font-bold">
                      {item.web_vulnerabilities.length}
                    </span>
                  ) : (
                    "-"
                  )}
                </td>

                <td className="p-4">
                  {item.risk?.recommendation || "-"}
                </td>

              </tr>
            ))}
          </tbody>

        </table>

      </div>
    </div>
  );
}

export default FindingsTable;