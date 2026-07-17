import React from 'react';

function TechnologyCard({ findings }) {
  const techFindings = findings.filter(
    item => item.technology
  );

  if (techFindings.length === 0)
    return null;

  return (
    <div className="space-y-6">
      {techFindings.map((finding) => {
        {/* Step 1: Safely fall back to empty object if technology is null/undefined */}
        const tech = finding.technology || {};

        return (
          <div
            key={finding.port}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6"
          >
            <h2 className="text-2xl font-bold text-cyan-400 mb-2">
              💻 Technology Detection
            </h2>

            <p className="text-gray-400 mb-6">
              Port {finding.port}
            </p>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <p className="text-gray-400 text-sm">
                  Web Server
                </p>
                {/* Step 2: Added "Unknown" safety fallback for all fields */}
                <p className="font-semibold">
                  {tech.server || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Language
                </p>
                <p className="font-semibold">
                  {tech.language || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Framework
                </p>
                <p className="font-semibold">
                  {tech.framework || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  CMS
                </p>
                <p className="font-semibold">
                  {tech.cms || "Unknown"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Frontend
                </p>
                <p className="font-semibold">
                  {tech.frontend || "Unknown"}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default TechnologyCard;