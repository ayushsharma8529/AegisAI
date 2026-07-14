function HostCard({ host }) {
  if (!host) return null;

  return (
    <div>
      <h2>Host Information</h2>

      <p><b>Hostname:</b> {host.hostname}</p>
      <p><b>Operating System:</b> {host.os_guess}</p>
      <p><b>Overall Risk:</b> {host.overall_risk}</p>
      <p><b>Open Ports:</b> {host.open_ports}</p>
    </div>
  );
}

export default HostCard;