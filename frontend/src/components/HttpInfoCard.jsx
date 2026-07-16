import React from 'react';

function HttpInfoCard({ findings }) {
  const httpFindings = findings.filter(
    item => item.http_info
  );

  if (httpFindings.length === 0)
    return null;

  return (
    <div className="space-y-6">
      {httpFindings.map((finding) => {
        const info = finding.http_info;

        return (
          <div 
            key={finding.port} 
            className="bg-gray-900 rounded-xl border border-gray-800 p-6 mb-6"
          >
            {/* UI Fix 1: Heading and Port text separated for a clean look */}
            <h2 className="text-2xl font-bold text-cyan-400 mb-2">
              🌐 HTTP Enumeration
            </h2>
            <p className="text-gray-400 mb-6">
              Port {finding.port}
            </p>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <p className="text-gray-400 text-sm">Title</p>
                <p className="font-semibold">
                  {info.title || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">Server</p>
                <p className="font-semibold">
                  {info.server || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">Powered By</p>
                <p className="font-semibold">
                  {info.powered_by || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">Redirect</p>
                {info.redirect ? (
                  <a
                    href={info.redirect}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 break-all hover:underline"
                  >
                    {info.redirect}
                  </a>
                ) : (
                  <p className="font-semibold">None</p>
                )}
              </div>

              <div className="md:col-span-2">
                <p className="text-gray-400 text-sm mb-2">
                  Cookies
                </p>
                <p className="font-semibold">
                  {info.cookies && info.cookies.length
                    ? info.cookies.join(", ")
                    : "No Cookies"}
                </p>
              </div>
            </div>

            <hr className="my-6 border-gray-700" />

            <h3 className="text-xl font-bold mb-4">
              Security Headers
            </h3>

            <div className="space-y-3">
              {info.security_headers && Object.entries(info.security_headers).map(
                ([header, exists]) => (
                  <div
                    key={header}
                    className="flex justify-between items-center bg-gray-800 rounded-lg px-4 py-3"
                  >
                    <span>{header}</span>
                    {/* UI Fix 2: Bright indicator badges for headers */}
                    <span
                      className={`font-bold ${
                        exists
                          ? "text-green-400"
                          : "text-red-400"
                      }`}
                    >
                      {exists ? "✔ Present" : "✘ Missing"}
                    </span>
                  </div>
                )
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default HttpInfoCard;