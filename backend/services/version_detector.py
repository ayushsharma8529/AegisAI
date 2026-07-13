import re


def detect_version(service, banner):

    info = {
        "product": service,
        "version": "Unknown",
        "vendor": "Unknown"
    }

    if banner == "No banner":
        return info

    # Apache
    match = re.search(r"Apache/?([0-9.]+)?", banner, re.I)
    if match:
        info["product"] = "Apache"
        info["vendor"] = "Apache Software Foundation"
        if match.group(1):
            info["version"] = match.group(1)
        return info

    # OpenSSH
    match = re.search(r"OpenSSH[_ ]([0-9.p]+)", banner, re.I)
    if match:
        info["product"] = "OpenSSH"
        info["vendor"] = "OpenBSD"
        info["version"] = match.group(1)
        return info

    # nginx
    match = re.search(r"nginx/?([0-9.]+)?", banner, re.I)
    if match:
        info["product"] = "nginx"
        info["vendor"] = "NGINX"
        if match.group(1):
            info["version"] = match.group(1)
        return info

    return info