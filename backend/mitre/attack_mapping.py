MITRE_MAPPING = {

    445: {
        "technique": "T1021.002",
        "name": "SMB/Windows Admin Shares",
        "tactic": "Lateral Movement"
    },

    3389: {
        "technique": "T1021.001",
        "name": "Remote Desktop Protocol",
        "tactic": "Lateral Movement"
    },

    22: {
        "technique": "T1021.004",
        "name": "SSH",
        "tactic": "Lateral Movement"
    },

    21: {
        "technique": "T1071",
        "name": "Application Layer Protocol",
        "tactic": "Command and Control"
    },

    443: {
    "technique": "T1190",
    "name": "Exploit Public-Facing Application",
    "tactic": "Initial Access"
     }

}


def get_mitre(port):

    return MITRE_MAPPING.get(
        port,
        {
            "technique": "Unknown",
            "name": "Unknown",
            "tactic": "Unknown"
        }
    )