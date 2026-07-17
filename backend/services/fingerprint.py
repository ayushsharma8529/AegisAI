def fingerprint_service(service, banner, port):

    info = {
        "product": service,
        "vendor": "Unknown",
        "technology": service,
        "confidence": "Low"
    }

    if not banner:
        banner = ""

    text = banner.lower()

    # VMware
    if "vmware" in text:
        info.update({
            "product": "VMware Authentication Daemon",
            "vendor": "VMware",
            "technology": "VMware",
            "confidence": "High"
        })

    # Apache
    elif "apache" in text:
        info.update({
            "product": "Apache HTTP Server",
            "vendor": "Apache Foundation",
            "technology": "Apache",
            "confidence": "High"
        })

    # nginx
    elif "nginx" in text:
        info.update({
            "product": "NGINX",
            "vendor": "NGINX",
            "technology": "NGINX",
            "confidence": "High"
        })

    # OpenSSH
    elif "openssh" in text:
        info.update({
            "product": "OpenSSH",
            "vendor": "OpenBSD",
            "technology": "SSH",
            "confidence": "High"
        })

    # Microsoft IIS
    elif "microsoft-iis" in text or "iis" in text:
        info.update({
            "product": "Microsoft IIS",
            "vendor": "Microsoft",
            "technology": "IIS",
            "confidence": "High"
        })

    # Google
    elif "google" in text or "gws" in text:
        info.update({
            "product": "Google Frontend",
            "vendor": "Google",
            "technology": "Google Web Server",
            "confidence": "Medium"
        })

    # Cloudflare
    elif "cloudflare" in text:
        info.update({
            "product": "Cloudflare",
            "vendor": "Cloudflare",
            "technology": "Reverse Proxy",
            "confidence": "High"
        })

    # Meta / Facebook
    elif "proxygen" in text:
        info.update({
            "product": "Meta Proxygen",
            "vendor": "Meta",
            "technology": "Proxygen",
            "confidence": "High"
        })

    # Service based detection
    elif service == "MICROSOFT-DS":
        info.update({
            "product": "Microsoft SMB",
            "vendor": "Microsoft",
            "technology": "SMB",
            "confidence": "Medium"
        })

    elif service == "EPMAP":
        info.update({
            "product": "RPC Endpoint Mapper",
            "vendor": "Microsoft",
            "technology": "RPC",
            "confidence": "Medium"
        })

    # Port based fallback
    elif port == 902:
        info.update({
            "product": "VMware ESXi",
            "vendor": "VMware",
            "technology": "Virtualization",
            "confidence": "Medium"
        })

    elif port == 912:
        info.update({
            "product": "VMware Authentication Daemon",
            "vendor": "VMware",
            "technology": "Virtualization",
            "confidence": "Medium"
        })

    return info