def generate_analysis(findings):

    if not findings:
        return (
            "No open ports were detected. "
            "The target appears to have a small exposed attack surface."
        )

    report = []

    for item in findings:

        report.append(
            f"Port {item['port']} ({item['service']}) is open with {item['severity']} severity."
        )

        report.append(
            item["risk"]["recommendation"]
        )

    return "\n".join(report)