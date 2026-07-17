function DirectoryCard({ findings }) {

  const directoryFindings = findings.filter(
    item => item.directories && item.directories.length > 0
  );

  if (directoryFindings.length === 0)
    return null;

  return (

    <div className="space-y-6">

      {directoryFindings.map((finding) => (

        <div
          key={finding.port}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >

          <h2 className="text-2xl font-bold text-cyan-400 mb-2">
            📂 Directory Enumeration
          </h2>

          <p className="text-gray-400 mb-6">
            Port {finding.port}
          </p>

          <table className="w-full">

            <thead>

              <tr className="text-left border-b border-gray-700">

                <th className="py-3">Path</th>

                <th>Status</th>

                <th>Redirect</th>

              </tr>

            </thead>

            <tbody>

              {finding.directories.map((dir, index) => (

                <tr
                  key={index}
                  className="border-b border-gray-800"
                >

                  <td className="py-3 font-mono">
                    {dir.path}
                  </td>

                  <td>

                    <span className="text-yellow-400 font-semibold">
                      {dir.status}
                    </span>

                  </td>

                  <td>

                    {dir.redirect ? (

                      <a
                        href={dir.redirect}
                        target="_blank"
                        rel="noreferrer"
                        className="text-cyan-400 hover:underline break-all"
                      >
                        {dir.redirect}
                      </a>

                    ) : (

                      "-"

                    )}

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      ))}

    </div>

  );

}

export default DirectoryCard;