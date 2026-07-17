import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

function ServiceChart({ findings }) {
  if (!findings) return null;

  const counts = {};

  findings.forEach((item) => {
    counts[item.service] = (counts[item.service] || 0) + 1;
  });

  const data = Object.keys(counts).map((service) => ({
    service,
    count: counts[service],
  }));

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        📊 Services
      </h2>

      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="service" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#06b6d4" />
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

export default ServiceChart;