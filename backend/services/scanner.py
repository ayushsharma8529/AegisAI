import ssl
import socket
from concurrent.futures import ThreadPoolExecutor
from services.banner import grab_banner
from services.risk_engine import analyze_risk
from mitre.attack_mapping import get_mitre
from services.version_detector import detect_version
from services.cve_lookup import lookup_cves
from services.host_info import get_host_information
from services.fingerprint import fingerprint_service
from enumeration.http_enum import enumerate_http
from enumeration.tls_enum import enumerate_tls
from services.technology_detector import detect_technology
from enumeration.directory_enum import enumerate_directories
from enumeration.http_methods import detect_http_methods
from services.web_vulnerability import check_web_vulnerabilities

SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}


def scan_port(target, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

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
        
        # --- DEBUG PRINTS (BANNER) ---
        print(f"\n===== PORT {port} =====")
        print("SERVICE:", service)
        print("BANNER:", banner[:150])

       
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
        # HTTP Enumeration
        http_info = None

        if port in [80, 443]:
            http_info = enumerate_http(target, port)

        # HTTP methods
        http_methods = None

        if port in [80, 443]:

           http_methods = detect_http_methods(
           target,
           port
        )

           print("\n===== HTTP METHODS =====")
           print(http_methods)

        #directory information
        directory_info = None

        if port in [80, 443]:
           directory_info = enumerate_directories(
           target,
           port
        )
           print("\n===== DIRECTORIES =====")
           print(directory_info)
        # Technology Detection
        technology = None

        if http_info:
          technology = detect_technology(
          http_info,
          banner
        )
          print("\n===== TECHNOLOGY =====")
          print(technology)
        # TLS Enumeration
        tls_info = None

        if port == 443:
            tls_info = enumerate_tls(target, port)    
            print("\n===== TLS INFO =====")
            print(tls_info)

        # web vulnerablility
        web_vulns = []

        if port in [80, 443]:
          web_vulns = check_web_vulnerabilities(
            target,
            port,
         )

          print("\n===== WEB VULNERABILITIES =====")
          print(web_vulns)

        # fingerprint
        fingerprint = fingerprint_service(
           service,
           banner,
           port
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
            "cves": cves,
            "fingerprint": fingerprint,
            "http_info": http_info,
            "tls_info": tls_info,
            "technology": technology,
            "directories": directory_info,
            "http_methods": http_methods,
            "web_vulnerabilities": web_vulns,
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

    # --- Step 1: Risk Score Calculation ---
    risk_score = 0
    for finding in findings:
        severity = finding.get("severity", "Low")

        if severity == "Critical":
            risk_score += 40
        elif severity == "High":
            risk_score += 20
        elif severity == "Medium":
            risk_score += 10
        else:
            risk_score += 3

        # Web Vulnerabilities score weightage
        risk_score += len(
            finding.get("web_vulnerabilities", [])
        ) * 2

    # Maximum 100 limit capped
    risk_score = min(risk_score, 100)

    host = get_host_information(target, findings)
    findings.sort(
      key=lambda x: x["risk"].get("risk_score", 0),
      reverse=True
    )

    # --- Step 2: Added risk_score in final response ---
    return {
        "target": target,
        "host": host,
        "status": "completed",
        "message": "Port scan executed successfully",
        "risk_score": risk_score,
        "findings": findings
    }