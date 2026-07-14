from datetime import datetime


def generate_html_report(scan_result):

    findings_html = ""

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
}}

th,td {{
border:1px solid #ccc;
padding:10px;
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