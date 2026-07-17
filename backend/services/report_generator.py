from datetime import datetime


def generate_html_report(scan_result):
    findings_html = ""
    
    # --- PHASE 2: Step 1 (Calculate Stats for Executive Summary) ---
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
    # ---------------------------------------------------------------

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

        findings_html += f"""
        <tr>
            <td>{item['port']}</td>
            <td>{item['service']}</td>
            <td>{item['severity']}</td>
            <td>{item['risk']['issue']}</td>
            <td>{item['mitre']['technique']}</td>
        </tr>

        <tr>
            <td colspan="5">
                <b>Recommendation:</b>
                {item['risk']['recommendation']}
                <br><br>

                <b>CVEs</b>

                <ul>
                    {cve_html}
                </ul>
            </td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AegisAI Report</title>
<style>
body {{
    font-family: Arial;
    background:#f4f4f4;
    padding:30px;
}}

table {{
    width:100%;
    border-collapse:collapse;
    background:white;
    margin-bottom: 20px;
}}

th,td {{
    border:1px solid #ccc;
    padding:10px;
    text-align: left;
}}

th {{
    background:#222;
    color:white;
}}

h1 {{
    color:#1f4e79;
}}
</style>
</head>
<body>

<h1>AegisAI Security Report</h1>

<p><b>Generated:</b> {datetime.now()}</p>
<p><b>Target:</b> {scan_result["target"]}</p>
<p><b>Status:</b> {scan_result["status"]}</p>

<!-- --- PHASE 2: Step 2 (Executive Summary Table Block) --- -->
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

<br>
<!-- ------------------------------------------------------ -->

<p><b>Summary</b></p>
<p>{scan_result["analysis"].replace(chr(10), "<br>")}</p>

<br>

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