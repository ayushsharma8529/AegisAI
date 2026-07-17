def analyze_risk(finding):
    # Default risk state
    risk = {
        "risk_level": "Low",
        "risk_score": 10,
        "issue": "Unknown service",
        "recommendation": "Review this service",
        "fix_priority": "Monitor",
        "business_impact": "Low"
    }

    port = finding.get("port")
    service = finding.get("service")

    if port == 445:
        risk = {
            "risk_level": "High",
            "risk_score": 85,
            "issue": "SMB service exposed",
            "recommendation": "Disable SMBv1 and restrict SMB access",
            "fix_priority": "Immediate",
            "business_impact": "High"
        }

    elif port == 3389:
        risk = {
            "risk_level": "High",
            "risk_score": 80,
            "issue": "RDP exposed",
            "recommendation": "Use MFA and restrict remote access",
            "fix_priority": "Immediate",
            "business_impact": "High"
        }

    elif port == 21:
        risk = {
            "risk_level": "Medium",
            "risk_score": 60,
            "issue": "FTP service detected",
            "recommendation": "Use SFTP instead of FTP",
            "fix_priority": "Soon",
            "business_impact": "Medium"
        }

    elif port == 22:
        risk = {
            "risk_level": "Medium",
            "risk_score": 45,
            "issue": "SSH service exposed",
            "recommendation": "Disable password login and use keys",
            "fix_priority": "Soon",
            "business_impact": "Medium"
        }

    elif port == 443:
        risk = {
            "risk_level": "Low",
            "risk_score": 20,
            "issue": "HTTPS service exposed",
            "recommendation": "Ensure TLS is up-to-date and disable weak ciphers",
            "fix_priority": "Monitor",
            "business_impact": "Low"
        }

    return risk