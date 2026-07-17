def calculate_risk_score(findings):

    score = 0

    for finding in findings:

        severity = finding.get("severity", "Low")

        if severity == "Critical":
            score += 40

        elif severity == "High":
            score += 20

        elif severity == "Medium":
            score += 10

        else:
            score += 3

        # Web Vulnerabilities
        score += len(
            finding.get("web_vulnerabilities", [])
        ) * 2

        # Dangerous Services
        if finding["port"] in [21, 23, 445, 3389]:
            score += 10

        # CVSS Based Weight
        for cve in finding.get("cves", []):

            cvss = cve.get("cvss", 0)

            if cvss >= 9:
                score += 25

            elif cvss >= 7:
                score += 15

            elif cvss >= 4:
                score += 8

            else:
                score += 3

    return min(score, 100)