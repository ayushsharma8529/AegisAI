function FindingsTable({ findings }) {
  if (!findings || findings.length === 0) {
    return null;
  }

  return (
    <div>
      <h2>Open Ports</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Severity</th>
          </tr>
        </thead>

        <tbody>
          {findings.map((item, index) => (
            <tr key={index}>
              <td>{item.port}</td>
              <td>{item.service}</td>
              <td>{item.severity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FindingsTable;