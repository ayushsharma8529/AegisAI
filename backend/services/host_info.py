import socket


def get_host_information(target, findings):

    info = {
        "alive": False,
        "ip": target,
        "hostname": "Unknown",
        "os_guess": "Unknown",
        "open_ports": len(findings),
        "overall_risk": "Low"
    }

    # ----------------------------
    # Hostname Detection
    # ----------------------------
    try:
        hostname = socket.gethostbyaddr(target)[0]

        if hostname and hostname != target:
            info["hostname"] = hostname

    except Exception:
        try:
            hostname = socket.getfqdn(target)

            if hostname and hostname != target:
                info["hostname"] = hostname

        except Exception:
            pass

    # ----------------------------
    # Alive Detection
    # ----------------------------
    if findings:
        info["alive"] = True

    # ----------------------------
    # Overall Risk
    # ----------------------------
    severities = [item["severity"] for item in findings]

    if "Critical" in severities:
        info["overall_risk"] = "Critical"

    elif "High" in severities:
        info["overall_risk"] = "High"

    elif "Medium" in severities:
        info["overall_risk"] = "Medium"

    else:
        info["overall_risk"] = "Low"

    # ----------------------------
    # OS Guess
    # ----------------------------
    ports = {item["port"] for item in findings}

    if {135, 139, 445}.intersection(ports):
        info["os_guess"] = "Windows"

    elif 22 in ports:
        info["os_guess"] = "Linux / Unix"

    elif 548 in ports:
        info["os_guess"] = "macOS"

    elif 80 in ports or 443 in ports:
        info["os_guess"] = "Network Device / Web Server"

    else:
        info["os_guess"] = "Unknown"

    return info