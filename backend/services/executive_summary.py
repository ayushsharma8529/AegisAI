def generate_executive_summary(scan):

    risk = scan["risk_score"]

    if risk >= 80:
        return (
            "Critical security issues detected. "
            "Immediate remediation is recommended."
        )

    elif risk >= 60:
        return (
            "Several high-risk services were identified. "
            "The attack surface should be reduced."
        )

    elif risk >= 30:
        return (
            "The target contains moderate security weaknesses. "
            "Security hardening is recommended."
        )

    else:
        return (
            "The target appears relatively secure. "
            "Only minor security issues were detected."
        )