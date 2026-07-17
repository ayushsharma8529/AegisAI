function TlsInfoCard({ findings }) {

  const tlsFindings = findings.filter(
    item => item.tls_info
  );

  if (tlsFindings.length === 0)
    return null;

  return (

    <div className="space-y-6">

      {tlsFindings.map((finding) => {

        const tls = finding.tls_info;

        return (

          <div
            key={finding.port}
            className="bg-gray-900 rounded-xl border border-gray-800 p-6"
          >

            <h2 className="text-2xl font-bold text-cyan-400 mb-2">
              🔒 TLS Information
            </h2>

            <p className="text-gray-400 mb-6">
              Port {finding.port}
            </p>

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <p className="text-gray-400 text-sm">
                  TLS Version
                </p>

                <p className="font-semibold">
                  {tls.tls_version}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Certificate Status
                </p>

                <p
                  className={`font-semibold ${
                    tls.valid
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >
                  {tls.valid ? "✔ Valid" : "✘ Invalid"}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Issuer
                </p>

                <p className="font-semibold">
                  {tls.issuer}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Subject
                </p>

                <p className="font-semibold break-all">
                  {tls.subject}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Expires
                </p>

                <p className="font-semibold">
                  {tls.expires}
                </p>
              </div>

              <div>
                <p className="text-gray-400 text-sm">
                  Days Remaining
                </p>

                <p
                  className={`font-semibold ${
                    tls.days_remaining < 30
                      ? "text-red-400"
                      : "text-green-400"
                  }`}
                >
                  {tls.days_remaining} Days
                </p>
              </div>

            </div>

          </div>

        );

      })}

    </div>

  );

}

export default TlsInfoCard;