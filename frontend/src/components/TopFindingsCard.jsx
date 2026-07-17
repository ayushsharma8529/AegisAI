function TopFindingsCard({ findings }) {

  if (!findings || findings.length === 0) return null;

  const sorted = [...findings]
    .sort(
      (a, b) =>
        (b.risk?.risk_score || 0) -
        (a.risk?.risk_score || 0)
    )
    .slice(0, 5);

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">

      <h2 className="text-2xl font-bold text-red-400 mb-6">
        🔥 Top Findings
      </h2>

      <div className="space-y-4">

        {sorted.map((item, index) => (

          <div
            key={index}
            className="border border-gray-700 rounded-lg p-4"
          >

            <div className="flex justify-between">

              <h3 className="font-semibold">
                {item.risk.issue}
              </h3>

              <span className="text-red-400 font-bold">
                {item.risk.risk_score}
              </span>

            </div>

            <p className="text-gray-400 mt-2">
              {item.risk.recommendation}
            </p>

            <p className="text-sm mt-2 text-yellow-400">
              Priority : {item.risk.fix_priority}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default TopFindingsCard;