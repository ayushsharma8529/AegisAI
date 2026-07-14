function HostCard({ host }) {
  if (!host) return null;

  const riskColor = {
    Critical: "bg-red-600",
    High: "bg-red-500",
    Medium: "bg-yellow-500",
    Low: "bg-green-500",
  };

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-lg">

      <h2 className="mb-6 text-2xl font-bold text-cyan-400">
        🖥 Host Information
      </h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">

        <div className="rounded-xl bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Hostname</p>
          <p className="text-lg font-semibold">{host.hostname}</p>
        </div>

        <div className="rounded-xl bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Operating System</p>
          <p className="text-lg font-semibold">{host.os_guess}</p>
        </div>
        <div className="rounded-xl bg-gray-800 p-4">
          <p className="text-sm text-gray-400">IP Address</p>
          <p className="text-lg font-semibold">{host.ip}</p>
        </div>


        <div className="rounded-xl bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Open Ports</p>
          <p className="text-lg font-semibold">{host.open_ports}</p>
        </div>

        <div className="rounded-xl bg-gray-800 p-4">
          <p className="text-sm text-gray-400 mb-2">
            Overall Risk
          </p>

          <span
            className={`rounded-full px-4 py-2 text-sm font-bold text-white ${
              riskColor[host.overall_risk] || "bg-gray-600"
            }`}
          >
            {host.overall_risk}
          </span>
        </div>

      </div>

    </div>
  );
}

export default HostCard;