from impacket.smbconnection import SMBConnection


def enumerate_smb(ip):
    result = {
        "service": "SMB",
        "reachable": False,
        "smb_version": "Unknown",
        "signing_required": "Unknown",
        "server_name": "Unknown",
        "domain": "Unknown"
    }

    try:
        conn = SMBConnection(ip, ip, sess_port=445)
        conn.login("", "")   # Anonymous login attempt

        result["reachable"] = True

        try:
            result["server_name"] = conn.getServerName()
        except:
            pass

        try:
            result["domain"] = conn.getServerDomain()
        except:
            pass

        try:
            if conn.doesSupportNTLMv2():
                result["smb_version"] = "SMB2/SMB3"
            else:
                result["smb_version"] = "SMB1"
        except:
            pass

        try:
            result["signing_required"] = conn.isSigningRequired()
        except:
            pass

        conn.logoff()

    except Exception as e:
        result["error"] = str(e)

    return result