import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from "recharts";

function RiskGauge({ score }) {

  const data = [
    {
      name: "Risk",
      value: score,
      fill:
        score >= 70
          ? "#ef4444"
          : score >= 40
          ? "#f59e0b"
          : "#22c55e",
    },
  ];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        🎯 Risk Score
      </h2>

      <div style={{ width: "100%", height: 280 }}>

        <ResponsiveContainer>

          <RadialBarChart
            innerRadius="70%"
            outerRadius="100%"
            data={data}
            startAngle={180}
            endAngle={0}
          >

            <PolarAngleAxis
              type="number"
              domain={[0, 100]}
              tick={false}
            />

            <RadialBar
              background
              clockWise
              dataKey="value"
            />

            <text
              x="50%"
              y="55%"
              textAnchor="middle"
              fill="white"
              fontSize="32"
              fontWeight="bold"
            >
              {score}
            </text>

          </RadialBarChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default RiskGauge;