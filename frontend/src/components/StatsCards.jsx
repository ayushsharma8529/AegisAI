import React from 'react';

function StatsCards({ result }) {
  if (!result) return null;

  const totalPorts = result.findings.length;

  const highRisk = result.findings.filter(
    (item) => item.severity === "High"
  ).length;

  const totalCVEs = result.findings.reduce(
    (count, item) => count + (item.cves?.length || 0),
    0
  );

  const totalWebVulns = result.findings.reduce(
    (count, item) => count + (item.web_vulnerabilities?.length || 0),
    0
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-6">

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400">Open Ports</p>
        <h2 className="text-3xl font-bold text-cyan-400">
          {totalPorts}
        </h2>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400">High Risk</p>
        <h2 className="text-3xl font-bold text-red-400">
          {highRisk}
        </h2>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400">CVEs Found</p>
        <h2 className="text-3xl font-bold text-yellow-400">
          {totalCVEs}
        </h2>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400">Web Vulnerabilities</p>
        <h2 className="text-3xl font-bold text-orange-400">
          {totalWebVulns}
        </h2>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400">Overall Risk</p>
        <h2 className="text-3xl font-bold text-purple-400">
          {result.host.overall_risk}
        </h2>
        
        {/* Step 3: Added dynamic Risk Score sub-card inside Overall Risk block */}
        <p className="text-gray-400 mt-3">
          Risk Score
        </p>
        <h3 className="text-xl font-bold text-red-400">
          {result.risk_score}/100
        </h3>
      </div>

    </div>
  );
}

export default StatsCards;