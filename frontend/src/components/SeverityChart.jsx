import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function SeverityChart({ findings }) {

  if (!findings || findings.length === 0) return null;

  const critical = findings.filter(
    (x) => x.severity === "Critical"
  ).length;

  const high = findings.filter(
    (x) => x.severity === "High"
  ).length;

  const medium = findings.filter(
    (x) => x.severity === "Medium"
  ).length;

  const low = findings.filter(
    (x) => x.severity === "Low"
  ).length;

  const data = [
    { name: "Critical", value: critical },
    { name: "High", value: high },
    { name: "Medium", value: medium },
    { name: "Low", value: low },
  ].filter((item) => item.value > 0);

  const COLORS = [
    "#991B1B",
    "#EF4444",
    "#FACC15",
    "#22C55E",
  ];

  return (

    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        📊 Severity Distribution
      </h2>

      <div style={{ width: "100%", height: 350 }}>

        <ResponsiveContainer>

          <PieChart>

            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              outerRadius={120}
              label
            >

              {data.map((entry, index) => (

                <Cell
                  key={index}
                  fill={COLORS[index]}
                />

              ))}

            </Pie>

            <Tooltip />

            <Legend />

          </PieChart>

        </ResponsiveContainer>

      </div>

    </div>

  );

}

export default SeverityChart;