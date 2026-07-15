import ssl
import socket
from concurrent.futures import ThreadPoolExecutor

from services.risk_engine import analyze_risk
from mitre.attack_mapping import get_mitre
from services.version_detector import detect_version
from services.cve_lookup import lookup_cves
from services.host_info import get_host_information



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

        # HTTP
        if port == 80:

            sock = socket.create_connection((target, port), timeout=2)

            sock.sendall(
                f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n".encode()
            )

            banner = sock.recv(4096).decode(errors="ignore")

            sock.close()

            return banner


        # HTTPS
        elif port == 443:

            context = ssl.create_default_context()

            raw = socket.create_connection((target, port), timeout=2)

            sock = context.wrap_socket(raw, server_hostname=target)

            sock.sendall(
                f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n".encode()
            )

            banner = sock.recv(4096).decode(errors="ignore")

            sock.close()

            return banner


        # Other protocols
        else:

            sock = socket.create_connection((target, port), timeout=2)

            banner = sock.recv(4096).decode(errors="ignore")

            sock.close()

            if banner:
                return banner

    except Exception:
        pass

    return "No banner"


def scan_port(target, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((target, port))
    except socket.gaierror:
        return None

    sock.close()

    if result == 0:

        # Service Detection
        try:
            service = socket.getservbyport(port).upper()
        except:
            service = SERVICES.get(port, "Unknown")

        # Severity
        severity = "Low"

        if port in [445, 3389]:
            severity = "High"

        elif port in [21, 22]:
            severity = "Medium"

        # Banner
        banner = grab_banner(target, port)

        # Version Detection
        version_info = detect_version(
            service,
            banner
        )

        # CVE Lookup
        cves = lookup_cves(
            version_info["product"],
            version_info["version"]
        )

        # Risk Engine
        risk = analyze_risk({
            "port": port,
            "service": service
        })

        # MITRE
        mitre = get_mitre(port)

        return {
            "port": port,
            "service": service,
            "status": "open",
            "severity": severity,
            "banner": banner,
            "version_info": version_info,
            "risk": risk,
            "mitre": mitre,
            "cves": cves
        }

    return None


def run_scan(target, start_port, end_port):
    print(target)
    print(start_port)
    print(end_port)
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

    host = get_host_information(target, findings)

    return {
        "target": target,
        "host": host,
        "status": "completed",
        "message": "Port scan executed successfully",
        "findings": findings
    }