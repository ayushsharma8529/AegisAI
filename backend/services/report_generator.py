from datetime import datetime

# --- Helper function to generate clean list items ---
def make_list(items):
    if not items:
        return "<li style='color: #64748b;'>None Detected</li>"
    return "".join(
        f"<li style='margin-bottom: 6px;'>{x}</li>"
        for x in items
    )

def generate_html_report(scan_result):
    findings_html = ""
    findings = scan_result.get("findings", [])
    
    # --- Executive Summary Calculations ---
    open_ports = len(findings)

    critical = sum(1 for f in findings if f.get("severity") == "Critical")
    high = sum(1 for f in findings if f.get("severity") == "High")
    medium = sum(1 for f in findings if f.get("severity") == "Medium")
    low = sum(1 for f in findings if f.get("severity") == "Low")

    web_vulns = sum(
        len(f.get("web_vulnerabilities", []))
        for f in findings
    )

    risk_score = scan_result.get("risk_score", 0)
    host_info = scan_result.get("host", {})
    overall_risk = host_info.get("overall_risk", "Low")

    # --- Grouping issues for Quick Overview ---
    high_findings = []
    medium_findings = []
    low_findings = []

    for item in findings:
        risk_data = item.get("risk", {})
        issue = risk_data.get("issue", "Unknown Issue")
        severity_check = item.get("severity", "Low")
        
        if severity_check in ["Critical", "High"]:
            high_findings.append(issue)
        elif severity_check == "Medium":
            medium_findings.append(issue)
        else:
            low_findings.append(issue)

    # --- MITRE Framework Matrix Integration ---
    mitre_summary_rows = ""
    for item in findings:
        mitre_data = item.get("mitre")
        risk_data = item.get("risk", {})
        if mitre_data:
            mitre_summary_rows += f"""
            <tr>
                <td style="font-weight: 600; color: #0f172a;">{mitre_data.get('id', 'N/A')}</td>
                <td><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em;">{mitre_data.get('technique', 'Unknown')}</code></td>
                <td>{risk_data.get('issue', 'Unknown Issue')}</td>
            </tr>
            """

    # --- Table Generation Loop ---
    for item in findings:
        risk_data = item.get("risk", {})
        mitre_data = item.get("mitre", {})
        
        # Inject structural dynamic heading for clarity per item
        findings_html += f"""
        <tr style="background-color: #f1f5f9;">
            <td colspan="5" style="padding: 12px 16px;">
                <h3 style="margin: 0; color: #0f172a;">Port {item.get('port')} ({item.get('service')}) Technical Sub-context</h3>
            </td>
        </tr>
        """

        # 1. HTTP Service Enumeration Block (with customized content length handler)
        http_html = ""
        if item.get("http_info"):
            http = item["http_info"]
            
            # Extract and filter content length
            raw_length = str(http.get("content_length", "Unknown"))
            content_length_display = "Redirect Response" if raw_length == "0" else raw_length
            
            # Sub-table parsing for Security Headers validation
            headers_row = ""
            if http.get("security_headers"):
                for header_name, status in http["security_headers"].items():
                    status_badge = '<span style="color: #16a34a; font-weight: bold;">✔ Pass</span>' if status else '<span style="color: #dc2626; font-weight: bold;">❌ Missing</span>'
                    headers_row += f"<tr><th>{header_name}</th><td>{status_badge}</td></tr>"
            
            security_headers_table = f"""
            <div style="margin-top: 15px;">
                <h5 style="margin-bottom: 5px; color: #475569;">Security Header Validation</h5>
                <table>{headers_row}</table>
            </div>
            """ if headers_row else ""

            http_html = f"""
            <div class="sub-section">
                <h4>HTTP Service Enumeration</h4>
                <table>
                    <tr><th style="width: 30%;">Page Title</th><td>{http.get("title", "Unknown")}</td></tr>
                    <tr><th>Server Banner</th><td>{http.get("server", "Unknown")}</td></tr>
                    <tr><th>Powered By</th><td>{http.get("powered_by", "Unknown")}</td></tr>
                    <tr><th>Redirection Target</th><td>{http.get("redirect", "None")}</td></tr>
                    <tr><th>Content Type</th><td>{http.get("content_type", "Unknown")}</td></tr>
                    <tr><th>Content Length</th><td>{content_length_display}</td></tr>
                    <tr><th>Cache Control</th><td>{http.get("cache_control", "Unknown")}</td></tr>
                    <tr><th>Entity Tag (ETag)</th><td>{http.get("etag", "Unknown")}</td></tr>
                    <tr><th>Via Proxy</th><td>{http.get("via", "Unknown")}</td></tr>
                    <tr><th>CMS / X-Generator</th><td>{http.get("x_generator", "Unknown")}</td></tr>
                </table>
                {security_headers_table}
            </div>
            """

        # 2. TLS Information Logic
        tls_html = ""
        if item.get("tls_info"):
            tls = item["tls_info"]
            tls_html = f"""
            <div class="sub-section">
                <h4>TLS/SSL Configuration</h4>
                <table>
                    <tr><th style="width: 30%;">TLS Cipher Protocol</th><td>{tls.get("tls_version", "Unknown")}</td></tr>
                    <tr><th>Certificate Chain Validity</th><td>{tls.get("certificate_status", "Unknown")}</td></tr>
                    <tr><th>Certificate Authority (Issuer)</th><td>{tls.get("issuer", "Unknown")}</td></tr>
                    <tr><th>Subject Identifier</th><td>{tls.get("subject", "Unknown")}</td></tr>
                    <tr><th>Expiration Date</th><td>{tls.get("expires", "Unknown")}</td></tr>
                    <tr><th>Days to Expiry</th><td>{tls.get("days_remaining", "Unknown")}</td></tr>
                </table>
            </div>
            """

        # 3. Technology Detection Logic
        tech_html = ""
        if item.get("technology"):
            tech = item["technology"]
            if any(v != "Unknown" for v in tech.values()):
                tech_html = f"""
                <div class="sub-section">
                    <h4>Technology Fingerprinting</h4>
                    <table>
                        <tr><th style="width: 30%;">Web Server Engine</th><td>{tech.get("web_server", "Unknown")}</td></tr>
                        <tr><th>Backend Language</th><td>{tech.get("language", "Unknown")}</td></tr>
                        <tr><th>Application Framework</th><td>{tech.get("framework", "Unknown")}</td></tr>
                        <tr><th>Content Management System</th><td>{tech.get("cms", "Unknown")}</td></tr>
                        <tr><th>Frontend Library</th><td>{tech.get("frontend", "Unknown")}</td></tr>
                    </table>
                </div>
                """

        # 4. Directory Enumeration Logic
        directory_html = ""
        if item.get("directories") and len(item["directories"]) > 0:
            rows = ""
            for d in item["directories"]:
                rows += f"""
                <tr>
                    <td><code>{d.get("path", "-")}</code></td>
                    <td><span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight:600;">{d.get("status", "-")}</span></td>
                    <td style="font-size: 0.9em; color: #475569;">{d.get("redirect", "None")}</td>
                </tr>
                """
            directory_html = f"""
            <div class="sub-section">
                <h4>Discovered Web Resources (Direct Responses)</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Identified Target Path</th>
                            <th>HTTP Response Status</th>
                            <th>Inbound Redirection Location</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """

        # 5. HTTP Methods Block (Optional Extension framework placeholder if passed)
        methods_html = ""
        if item.get("http_methods"):
            methods_html = f"""
            <div class="sub-section">
                <h4>Allowed HTTP Methods</h4>
                <p style="color: #334155; margin: 0;">{", ".join(item.get("http_methods", []))}</p>
            </div>
            """

        # 6. Web Vulnerabilities Logic
        vuln_html = ""
        if item.get("web_vulnerabilities"):
            rows = ""
            for vuln in item["web_vulnerabilities"]:
                v_sev = vuln.get("severity", "Low")
                v_color = "#dc2626" if v_sev in ["High", "Critical"] else ("#d97706" if v_sev == "Medium" else "#16a34a")
                rows += f"""
                <tr>
                    <td style="font-weight: 600;">{vuln.get("name", "Unknown")}</td>
                    <td><span style="color: {v_color}; font-weight: bold;">{v_sev}</span></td>
                    <td style="color: #334155;">{vuln.get("description", "-")}</td>
                </tr>
                """
            vuln_html = f"""
            <div class="sub-section">
                <h4>Application Security Anomalies</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Vulnerability Domain</th>
                            <th>Severity Assessment</th>
                            <th>Impact Context & Remediation Notes</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """

        # 7. CVE Section Configuration
        cve_section = ""
        if item.get("cves") and len(item["cves"]) > 0:
            cve_html = ""
            for cve in item["cves"]:
                cve_html += f"""
                <li style="margin-bottom: 5px;">
                    <strong style="color: #ef4444;">{cve.get('id', 'CVE-Unknown')}</strong> - {cve.get('name', 'N/A')} 
                    <span class="badge" style="background: #fee2e2; color: #ef4444; font-size: 0.8em; padding: 2px 8px;">CVSS {cve.get('cvss', 'N/A')}</span>
                </li>
                """
            cve_section = f"""
            <div class="sub-section">
                <h4>Linked Vulnerabilities & CVEs</h4>
                <ul>{cve_html}</ul>
            </div>
            """

        # Dynamic Severity Colors & Badges
        severity = item.get("severity", "Low")
        if severity == "Critical":
            color = "#dc2626"
            bg_color = "#fef2f2"
        elif severity == "High":
            color = "#ea580c"
            bg_color = "#fff7ed"
        elif severity == "Medium":
            color = "#d97706"
            bg_color = "#fef3c7"
        else:
            color = "#16a34a"
            bg_color = "#f0fdf4"

        # Structural Row Generation (Nested properly inside the Technical Table view)
        findings_html += f"""
        <tr class="main-row">
            <td style="font-weight: 600;">{item.get('port')}</td>
            <td><code style="background: #f1f5f9; padding: 3px 6px; border-radius: 4px;">{item.get('service')}</code></td>
            <td>
                <span class="badge" style="background: {bg_color}; color: {color}; border: 1px solid {color}40;">
                    {severity}
                </span>
            </td>
            <td style="font-weight: 500; color: #0f172a;">{risk_data.get('issue', 'N/A')}</td>
            <td><small style="color: #64748b;">{mitre_data.get('technique', 'N/A')}</small></td>
        </tr>
        <tr class="detail-row">
            <td colspan="5">
                <div style="padding: 10px 5px;">
                    <p style="margin-top:0;"><strong>Remediation Strategy:</strong> {risk_data.get('recommendation', 'N/A')}</p>
                    {http_html}
                    {tls_html}
                    {tech_html}
                    {directory_html}
                    {methods_html}
                    {vuln_html}
                    {cve_section}
                </div>
            </td>
        </tr>
        """

    # --- HTML Base Template Layout ---
    analysis_text = scan_result.get("analysis", "No analysis provided.").replace('\n', '<br>')
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AegisAI Executive & Technical Security Assessment Report</title>
<style>
    :root {{
        --primary: #0f172a;
        --secondary: #2563eb;
        --accent: #3b82f6;
        --bg-main: #f8fafc;
        --border-color: #e2e8f0;
        --text-dark: #1e293b;
        --text-light: #64748b;
    }}
    body {{
        background: var(--bg-main);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: var(--text-dark);
        line-height: 1.5;
        padding: 40px;
        margin: 0;
    }}
    .container {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    .header-card {{
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid var(--border-color);
        margin-bottom: 30px;
    }}
    .header-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }}
    .meta-item {{
        background: var(--bg-main);
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }}
    .meta-label {{
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-light);
        margin-bottom: 4px;
        font-weight: 600;
    }}
    .meta-val {{
        font-size: 1.1em;
        font-weight: 600;
        color: var(--primary);
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0 25px 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        border: 1px solid var(--border-color);
    }}
    th {{
        background: var(--primary);
        color: white;
        padding: 12px 16px;
        font-weight: 600;
        text-align: left;
        font-size: 0.95em;
    }}
    td {{
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-color);
        font-size: 0.95em;
    }}
    .main-row {{
        background: #ffffff;
    }}
    .detail-row {{
        background: #fdfdfd;
    }}
    .detail-row td {{
        border-bottom: 2px solid var(--border-color);
        background-color: #fafafa;
    }}
    .sub-section {{
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 20px;
        margin: 15px 0;
    }}
    .sub-section h4 {{
        margin-top: 0;
        margin-bottom: 15px;
        color: var(--primary);
        border-left: 4px solid var(--secondary);
        padding-left: 10px;
        font-size: 1.1em;
    }}
    .sub-section table {{
        margin: 0;
        box-shadow: none;
    }}
    .sub-section th {{
        background: #f1f5f9;
        color: var(--text-dark);
        font-weight: 600;
        width: 35%;
        border-bottom: 1px solid var(--border-color);
    }}
    h1 {{
        color: var(--primary);
        font-size: 2.2em;
        margin: 0 0 10px 0;
        font-weight: 700;
    }}
    h2 {{
        color: var(--primary);
        font-size: 1.6em;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 8px;
    }}
    h3 {{
        font-size: 1.2em;
        margin-top: 20px;
        margin-bottom: 10px;
        color: var(--primary);
    }}
    .badge {{
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
    }}
    .summary-box {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }}
    .stat-card {{
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01);
    }}
    .stat-num {{
        font-size: 1.8em;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 2px;
    }}
    .stat-label {{
        font-size: 0.85em;
        color: var(--text-light);
        font-weight: 500;
    }}
    ul {{
        padding-left: 20px;
        margin: 5px 0;
    }}
    .footer {{
        margin-top: 60px;
        border-top: 1px solid var(--border-color);
        padding-top: 20px;
        font-size: 0.85em;
        color: var(--text-light);
        text-align: center;
    }}
    @media print {{
        body {{ background: white; padding: 0; }}
        .container {{ width: 100%; max-width: 100%; }}
        .sub-section, .header-card, .stat-card {{ box-shadow: none !important; page-break-inside: avoid; }}
        tr {{ page-break-inside: avoid; }}
    }}
</style>
</head>
<body>

<div class="container">

    <!-- Top Assessment Metadata Card -->
    <div class="header-card">
        <h1>AegisAI Security Assessment Report</h1>
        <div class="header-grid">
            <div class="meta-item">
                <div class="meta-label">Target Scope</div>
                <div class="meta-val">{scan_result.get("target", "N/A")}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Generated Timestamp</div>
                <div class="meta-val">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Assessment Status</div>
                <div class="meta-val" style="color: #16a34a;">{scan_result.get("status", "Completed")}</div>
            </div>
        </div>
    </div>

    <!-- Executive Summary Dashboard Metrics -->
    <h2>1. Executive Summary</h2>
    <div class="summary-box">
        <div class="stat-card" style="border-top: 4px solid var(--secondary);">
            <div class="stat-num">{risk_score}<span style="font-size:0.5em; color:var(--text-light);">/100</span></div>
            <div class="stat-label">Risk Index</div>
        </div>
        <div class="stat-card" style="border-top: 4px solid #ef4444;">
            <div class="stat-num">{critical + high}</div>
            <div class="stat-label">High/Crit Threats</div>
        </div>
        <div class="stat-card" style="border-top: 4px solid #f59e0b;">
            <div class="stat-num">{medium}</div>
            <div class="stat-label">Medium Threats</div>
        </div>
        <div class="stat-card" style="border-top: 4px solid #10b981;">
            <div class="stat-num">{low}</div>
            <div class="stat-label">Low Anomalies</div>
        </div>
        <div class="stat-card" style="border-top: 4px solid #6366f1;">
            <div class="stat-num">{web_vulns}</div>
            <div class="stat-label">Web Vulnerabilities</div>
        </div>
    </div>

    <!-- Host Infrastructure Profile -->
    <h3>Target Infrastructure Profile</h3>
    <table>
        <tr><th style="width: 30%; background:#334155;">Identified Hostname</th><td>{host_info.get("hostname", "N/A")}</td></tr>
        <tr><th style="background:#334155;">Target IP Address</th><td>{host_info.get("ip", "N/A")}</td></tr>
        <tr><th style="background:#334155;">Fingerprinted OS</th><td>{host_info.get("os_guess", "Unknown")}</td></tr>
        <tr><th style="background:#334155;">Active Perimeter Interfaces</th><td>{host_info.get("open_ports", 0)} Open Ports</td></tr>
        <tr><th style="background:#334155;">Global Criticality Rating</th><td><strong>{overall_risk}</strong></td></tr>
        <tr><th style="background:#334155;">Network Accessibility</th><td>{ 'Active / Online' if host_info.get("alive") else 'No Response' }</td></tr>
    </table>

    <!-- Vulnerability Categorization Lists -->
    <h2>2. High-Level Vulnerability Review</h2>
    
    <h3 style="color: #dc2626;">🔴 Severe & Critical Findings</h3>
    <ul>{make_list(high_findings)}</ul>

    <h3 style="color: #d97706;">🟡 Moderate Risk Factors</h3>
    <ul>{make_list(medium_findings)}</ul>

    <h3 style="color: #16a34a;">🟢 Informational / Low Risk Metrics</h3>
    <ul>{make_list(low_findings)}</ul>

    <!-- MITRE Framework Threat Matrix -->
    {f'''
    <h2>3. MITRE ATT&CK Framework Mapping</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">Tactics ID</th>
                <th style="width: 30%;">Technique Identifier</th>
                <th>Mapped Security Finding</th>
            </tr>
        </thead>
        <tbody>
            {mitre_summary_rows}
        </tbody>
    </table>
    ''' if mitre_summary_rows else ''}

    <!-- Strategic AI Analysis Segment -->
    <h2>4. Strategic Threat Analysis</h2>
    <div style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.01);">
        <p style="margin: 0; color: #334155; text-align: justify;">{analysis_text}</p>
    </div>

    <!-- Deep Technical Deep-Dive Grid -->
    <h2>5. Technical Findings & Port Breakdown</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">Port</th>
                <th style="width: 15%;">Service</th>
                <th style="width: 15%;">Severity</th>
                <th style="width: 45%;">Identified Issue</th>
                <th style="width: 15%;">MITRE</th>
            </tr>
        </thead>
        <tbody>
            {findings_html}
        </tbody>
    </table>

    <!-- System Generated Footer -->
    <div class="footer">
        <p>CONFIDENTIAL | Generated by AegisAI Corporate Cyber Security Threat Engine.</p>
        <p>This document contains proprietary information intended solely for risk mitigation operations.</p>
    </div>

</div>

</body>
</html>
"""
    return html