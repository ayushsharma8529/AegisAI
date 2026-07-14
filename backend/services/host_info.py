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

    try:
        info["hostname"] = socket.gethostbyaddr(target)[0]
    except:
        pass

    if findings:
        info["alive"] = True

    severities = [item["severity"] for item in findings]

    if "High" in severities:
        info["overall_risk"] = "High"
    elif "Medium" in severities:
        info["overall_risk"] = "Medium"

    ports = [item["port"] for item in findings]

    if 445 in ports or 3389 in ports:
        info["os_guess"] = "Windows"
    elif 22 in ports:
        info["os_guess"] = "Linux/Unix"

    return info