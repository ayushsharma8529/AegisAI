def generate_analysis(findings):

    if not findings:
        return (
            "No open ports were detected. "
            "The target appears to have a small exposed attack surface."
        )

    report = []

    for item in findings:

        report.append(
            f"Port {item['port']} ({item['service']}) is open."
        )

        report.append(
            f"Severity: {item['severity']}"
        )

        report.append(
            f"Issue: {item['risk']['issue']}"
        )

        report.append(
            f"Recommendation: {item['risk']['recommendation']}"
        )

        if item["mitre"]:
            report.append(
                f"MITRE ATT&CK: {item['mitre']['technique']} - {item['mitre']['name']} ({item['mitre']['tactic']})"
            )

        if item["cves"]:

            report.append("Known Vulnerabilities:")

            for cve in item["cves"]:

                report.append(
                    f"- {cve['id']} ({cve['severity']}, CVSS {cve['cvss']}): {cve['name']}"
                )

                report.append(
                    f"  {cve['description']}"
                )

        report.append("")

    return "\n".join(report)