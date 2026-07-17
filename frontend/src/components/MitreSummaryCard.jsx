function MitreSummaryCard({ findings }) {
  if (!findings) return null;

  const techniques = {};

  findings.forEach((item) => {
    if (!item.mitre) return;

    const id = item.mitre.technique || "Unknown";

    techniques[id] = {
      id,
      tactic: item.mitre.tactic || "Unknown",
      name: item.mitre.name || "Unknown",
      count: (techniques[id]?.count || 0) + 1,
    };
  });

  const data = Object.values(techniques);

  if (data.length === 0) return null;

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        🎯 MITRE ATT&CK Summary
      </h2>

      <table className="w-full">

        <thead>
          <tr className="border-b border-gray-700">
            <th className="text-left p-3">Technique</th>
            <th className="text-left p-3">Name</th>
            <th className="text-left p-3">Tactic</th>
            <th className="text-left p-3">Count</th>
          </tr>
        </thead>

        <tbody>

          {data.map((item) => (

            <tr
              key={item.id}
              className="border-b border-gray-800"
            >

              <td className="p-3 font-semibold text-cyan-300">
                {item.id}
              </td>

              <td className="p-3">
                {item.name}
              </td>

              <td className="p-3">
                {item.tactic}
              </td>

              <td className="p-3">
                {item.count}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default MitreSummaryCard;