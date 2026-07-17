function RiskBreakdownCard({ findings }) {

  if (!findings) return null;

  const critical = findings.filter(
    x => x.severity === "Critical"
  ).length;

  const high = findings.filter(
    x => x.severity === "High"
  ).length;

  const medium = findings.filter(
    x => x.severity === "Medium"
  ).length;

  const low = findings.filter(
    x => x.severity === "Low"
  ).length;

  return (

    <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">

      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        📊 Risk Breakdown
      </h2>

      <div className="grid grid-cols-2 gap-4">

        <div className="bg-red-700 rounded-lg p-4">
          <p>Critical</p>
          <h2 className="text-3xl font-bold">{critical}</h2>
        </div>

        <div className="bg-red-500 rounded-lg p-4">
          <p>High</p>
          <h2 className="text-3xl font-bold">{high}</h2>
        </div>

        <div className="bg-yellow-500 text-black rounded-lg p-4">
          <p>Medium</p>
          <h2 className="text-3xl font-bold">{medium}</h2>
        </div>

        <div className="bg-green-600 rounded-lg p-4">
          <p>Low</p>
          <h2 className="text-3xl font-bold">{low}</h2>
        </div>

      </div>

    </div>

  );

}

export default RiskBreakdownCard;