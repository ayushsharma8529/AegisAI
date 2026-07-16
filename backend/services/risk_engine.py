def analyze_risk(finding):

    risk = {
        "risk_level": "Low",
        "issue": "Unknown service",
        "recommendation": "Review this service"
    }


    port = finding.get("port")
    service = finding.get("service")


    if port == 445:
        risk = {
            "risk_level": "High",
            "issue": "SMB service exposed",
            "recommendation": "Disable SMBv1 and restrict SMB access"
        }


    elif port == 3389:
        risk = {
            "risk_level": "High",
            "issue": "RDP exposed",
            "recommendation": "Use MFA and restrict remote access"
        }


    elif port == 21:
        risk = {
            "risk_level": "Medium",
            "issue": "FTP service detected",
            "recommendation": "Use SFTP instead of FTP"
        }


    elif port == 22:
        risk = {
            "risk_level": "Medium",
            "issue": "SSH service exposed",
            "recommendation": "Disable password login and use keys"
        }
    elif port ==443:
        risk ={
    "risk_level": "Low",
    "issue": "HTTPS service exposed",
    "recommendation": "Ensure TLS is up-to-date and disable weak ciphers"
}


    return risk