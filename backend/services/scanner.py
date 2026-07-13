import socket
from concurrent.futures import ThreadPoolExecutor
from services.risk_engine import analyze_risk
from mitre.attack_mapping import get_mitre


SERVICES = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}


def grab_banner(target, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        sock.connect((target, port))

        banner = sock.recv(1024).decode(errors="ignore")

        sock.close()

        if banner:
            return banner.strip()

    except:
        pass

    return "No banner"



def scan_port(target, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    sock.close()


    if result == 0:

        service = SERVICES.get(port, "Unknown")

        severity = "Low"

        if port in [445, 3389]:
            severity = "High"

        elif port in [21, 22]:
            severity = "Medium"


        banner = grab_banner(target, port)


        risk = analyze_risk({
            "port": port,
            "service": service
        })
        mitre = get_mitre(port)


        return {
            "port": port,
            "service": service,
            "status": "open",
            "severity": severity,
            "banner": banner,
            "risk": risk,
            "mitre": mitre
        }


    return None



def run_scan(target, start_port, end_port):

    findings = []

    ports = range(start_port, end_port + 1)


    with ThreadPoolExecutor(max_workers=50) as executor:

        results = executor.map(
            lambda port: scan_port(target, port),
            ports
        )


    for result in results:

        if result:
            findings.append(result)


    return {
        "target": target,
        "status": "completed",
        "message": "Port scan executed successfully",
        "findings": findings
    }