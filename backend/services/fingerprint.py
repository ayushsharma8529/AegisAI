def fingerprint_service(service, banner):

    info = {
        "product": service,
        "vendor": "Unknown",
        "technology": service,
        "confidence": "Low"
    }

    if not banner:
        return info

    text = banner.lower()

    # Apache
    if "apache" in text:
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

    # IIS
    elif "microsoft-iis" in text or "iis" in text:
        info.update({
            "product": "Microsoft IIS",
            "vendor": "Microsoft",
            "technology": "IIS",
            "confidence": "High"
        })

    # Google Frontend
    elif "google" in text:
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

    # SMB
    elif service == "MICROSOFT-DS":
        info.update({
            "product": "Microsoft SMB",
            "vendor": "Microsoft",
            "technology": "SMB",
            "confidence": "Medium"
        })

    # RPC
    elif service == "EPMAP":
        info.update({
            "product": "RPC Endpoint Mapper",
            "vendor": "Microsoft",
            "technology": "RPC",
            "confidence": "Medium"
        })
    elif  "proxygen" in text:
        info.update({
        "product": "Meta Proxygen",
        "vendor": "Meta",
        "technology": "Proxygen",
        "confidence": "High"
    })

    return info