from datetime import datetime


# --- PHASE 9: Step 2 (Helper function to generate clean list items) ---
def make_list(items):
    if not items:
        return "<li>None</li>"
    return "".join(
        f"<li>{x}</li>"
        for x in items
    )


def generate_html_report(scan_result):
    findings_html = ""
    
    # --- PHASE 2: Calculations for Executive Summary ---
    open_ports = len(scan_result["findings"])

    high = sum(
        1 for f in scan_result["findings"]
        if f["severity"] == "High"
    )

    medium = sum(
        1 for f in scan_result["findings"]
        if f["severity"] == "Medium"
    )

    low = sum(
        1 for f in scan_result["findings"]
        if f["severity"] == "Low"
    )

    web_vulns = sum(
        len(f.get("web_vulnerabilities", []))
        for f in scan_result["findings"]
    )

    risk_score = scan_result.get("risk_score", 0)
    overall_risk = scan_result["host"]["overall_risk"]

    # --- PHASE 9: Step 1 (Grouping issues for Quick Overview) ---
    high_findings = []
    medium_findings = []
    low_findings = []

    for item in scan_result["findings"]:
        issue = item["risk"]["issue"]
        
        # Checking severity to push issues in their respective buckets
        if item["severity"] == "High":
            high_findings.append(issue)
        elif item["severity"] == "Medium":
            medium_findings.append(issue)
        else:
            low_findings.append(issue)

    # --- Table generation loop ---
    for item in scan_result["findings"]:
        cve_html = ""

        for cve in item["cves"]:
            cve_html += f"""
            <li>
                <b>{cve['id']}</b> -
                {cve['name']}
                (CVSS {cve['cvss']})
            </li>
            """

        # --- PHASE 10: Step 1 (Severity Dynamic Colors) ---
        severity = item["severity"]

        if severity == "Critical":
            color = "#dc2626"
        elif severity == "High":
            color = "#ea580c"
        elif severity == "Medium":
            color = "#facc15"
        else:
            color = "#16a34a"

        # --- PHASE 11 (Part 2): Step 1 (HTTP Enumeration Logic) ---
        http_html = ""
        if item.get("http_info"):
            headers = item["http_info"].get("headers", {})
            http_html = f"""
            <br>
            <h4>HTTP Enumeration</h4>
            <table>
            <tr><th style="width: 30%;">Title</th><td>{item["http_info"].get("title", "N/A")}</td></tr>
            <tr><th>Server</th><td>{headers.get("Server", "Unknown")}</td></tr>
            <tr><th>Powered By</th><td>{headers.get("X-Powered-By", "Unknown")}</td></tr>
            <tr><th>Redirect</th><td>{item["http_info"].get("redirect", "None")}</td></tr>
            </table>
            """

        # --- TLS Information Logic ---
        tls_html = ""
        if item.get("tls_info"):
            tls = item["tls_info"]
            tls_html = f"""
            <br>
            <h4>TLS Information</h4>
            <table>
            <tr>
                <th style="width: 30%;">TLS Version</th>
                <td>{tls.get("tls_version", "Unknown")}</td>
            </tr>
            <tr>
                <th>Certificate Status</th>
                <td>{tls.get("certificate_status", "Unknown")}</td>
            </tr>
            <tr>
                <th>Issuer</th>
                <td>{tls.get("issuer", "Unknown")}</td>
            </tr>
            <tr>
                <th>Subject</th>
                <td>{tls.get("subject", "Unknown")}</td>
            </tr>
            <tr>
                <th>Expires</th>
                <td>{tls.get("expires", "Unknown")}</td>
            </tr>
            <tr>
                <th>Days Remaining</th>
                <td>{tls.get("days_remaining", "Unknown")}</td>
            </tr>
            </table>
            """

        # --- Technology Detection Logic ---
        tech_html = ""
        if item.get("technology"):
            tech = item["technology"]
            tech_html = f"""
            <br>
            <h4>Technology Detection</h4>
            <table>
            <tr>
                <th style="width: 30%;">Web Server</th>
                <td>{tech.get("web_server", "Unknown")}</td>
            </tr>
            <tr>
                <th>Language</th>
                <td>{tech.get("language", "Unknown")}</td>
            </tr>
            <tr>
                <th>Framework</th>
                <td>{tech.get("framework", "Unknown")}</td>
            </tr>
            <tr>
                <th>CMS</th>
                <td>{tech.get("cms", "Unknown")}</td>
            </tr>
            <tr>
                <th>Frontend</th>
                <td>{tech.get("frontend", "Unknown")}</td>
            </tr>
            </table>
            """

        # --- Directory Enumeration Logic ---
        directory_html = ""
        if item.get("directories"):
            rows = ""
            for d in item["directories"]:
                rows += f"""
                <tr>
                    <td>{d.get("path", "-")}</td>
                    <td>{d.get("status", "-")}</td>
                    <td>{d.get("redirect", "None")}</td>
                </tr>
                """
            directory_html = f"""
            <br>
            <h4>Directory Enumeration</h4>
            <table>
            <tr>
                <th>Path</th>
                <th>Status</th>
                <th>Redirect</th>
            </tr>
            {rows}
            </table>
            """

        # --- Web Vulnerabilities Logic ---
        vuln_html = ""
        if item.get("web_vulnerabilities"):
            rows = ""
            for vuln in item["web_vulnerabilities"]:
                rows += f"""
                <tr>
                    <td>{vuln.get("name", "Unknown")}</td>
                    <td>{vuln.get("severity", "Low")}</td>
                    <td>{vuln.get("description", "-")}</td>
                </tr>
                """
            vuln_html = f"""
            <br>
            <h4>Web Vulnerabilities</h4>
            <table>
            <tr>
                <th>Vulnerability</th>
                <th>Severity</th>
                <th>Description</th>
            </tr>
            {rows}
            </table>
            """

        # --- Data Placement inside Nested Technical Row ---
        findings_html += f"""
        <tr>
            <td>{item['port']}</td>
            <td>{item['service']}</td>
            <td>
                <span style="
                    background:{color};
                    padding:5px 12px;
                    border-radius:20px;
                    color:white;
                    font-weight:bold;
                    display:inline-block;
                ">
                    {severity}
                </span>
            </td>
            <td>{item['risk']['issue']}</td>
            <td>{item['mitre']['technique']}</td>
        </tr>

        <tr>
            <td colspan="5">
                <b>Recommendation:</b>
                {item['risk']['recommendation']}
                <br>
                
                {http_html}
                
                {tls_html}
                
                {tech_html}
                
                {directory_html}
                
                {vuln_html}
                <br>

                <b>CVEs</b>

                <ul>
                    {cve_html}
                </ul>
            </td>
        </tr>
        """

    # --- HTML Base Template Layout with your Updated CSS Styles ---
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AegisAI Report</title>
<style>
body {{
    background: #f3f6fb;
    font-family: Segoe UI,Arial,sans-serif;
    color: #222;
    line-height: 1.6;
    padding: 40px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,.08);
}}

th {{
    background: #0f172a;
    color: white;
    padding: 14px;
    text-align: left;
}}

td {{
    padding: 12px;
    border-bottom: 1px solid #eee;
    text-align: left;
}}

h1 {{
    color: #0f172a;
    font-size: 34px;
}}

h2 {{
    color: #2563eb;
    margin-top: 35px;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 8px;
}}

h3 {{
    margin-top: 15px;
    margin-bottom: 5px;
}}

h4 {{
    margin-top: 25px;
    color: #0f172a;
    margin-bottom: 8px;
}}

ul {{
    margin-top: 5px;
    padding-left: 20px;
}}

li {{
    padding: 3px 0;
}}
</style>
</head>
<body>

<h1>AegisAI Security Report</h1>

<p><b>Generated:</b> {datetime.now()}</p>
<p><b>Target:</b> {scan_result["target"]}</p>
<p><b>Status:</b> {scan_result["status"]}</p>

<hr>

<h2>Executive Summary</h2>

<table>
<tr>
    <th style="width: 30%;">Risk Score</th>
    <td>{risk_score}/100</td>
</tr>
<tr>
    <th>Overall Risk</th>
    <td>{overall_risk}</td>
</tr>
<tr>
    <th>Open Ports</th>
    <td>{open_ports}</td>
</tr>
<tr>
    <th>High Severity</th>
    <td>{high}</td>
</tr>
<tr>
    <th>Medium Severity</th>
    <td>{medium}</td>
</tr>
<tr>
    <th>Low Severity</th>
    <td>{low}</td>
</tr>
<tr>
    <th>Web Vulnerabilities</th>
    <td>{web_vulns}</td>
</tr>
</table>

<!-- --- Host Information Table --- -->
<h2>Host Information</h2>

<table>
<tr>
<th style="width: 30%;">Hostname</th>
<td>{scan_result["host"]["hostname"]}</td>
</tr>
<tr>
<th>IP Address</th>
<td>{scan_result["host"]["ip"]}</td>
</tr>
<tr>
<th>Operating System</th>
<td>{scan_result["host"]["os_guess"]}</td>
</tr>
<tr>
<th>Open Ports</th>
<td>{scan_result["host"]["open_ports"]}</td>
</tr>
<tr>
<th>Overall Risk</th>
<td>{scan_result["host"]["overall_risk"]}</td>
</tr>
<tr>
<th>Host Alive</th>
<td>{scan_result["host"]["alive"]}</td>
</tr>
</table>

<!-- --- Key Findings Section --- -->
<h2>Key Findings</h2>

<h3>🔴 High Risk</h3>
<ul>
{make_list(high_findings)}
</ul>

<h3>🟡 Medium Risk</h3>
<ul>
{make_list(medium_findings)}
</ul>

<h3>🟢 Low Risk</h3>
<ul>
{make_list(low_findings)}
</ul>

<hr>

<h2>AI Analysis</h2>
<p>{scan_result["analysis"].replace(chr(10), "<br>")}</p>

<br>

<h2>Technical Findings</h2>
<table>
<tr>
    <th>Port</th>
    <th>Service</th>
    <th>Severity</th>
    <th>Issue</th>
    <th>MITRE</th>
</tr>
{findings_html}
</table>

</body>
</html>
"""

    return html