CVE_DATABASE = {
    ("SMB", "Unknown"): [
        {
            "id": "CVE-2017-0144",
            "name": "EternalBlue",
            "severity": "Critical",
            "cvss": 9.8,
            "description": "SMBv1 Remote Code Execution vulnerability."
        }
    ],

    ("Apache", "2.4.49"): [
        {
            "id": "CVE-2021-41773",
            "name": "Apache Path Traversal",
            "severity": "Critical",
            "cvss": 9.8,
            "description": "Path traversal and possible remote code execution."
        }
    ],

    ("OpenSSH", "8.2"): [
        {
            "id": "CVE-2020-14145",
            "name": "OpenSSH Information Leak",
            "severity": "Medium",
            "cvss": 5.9,
            "description": "Information disclosure vulnerability."
        }
    ]
}


def lookup_cves(product, version):
    return CVE_DATABASE.get((product, version), [])