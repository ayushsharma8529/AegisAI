import ssl
import socket
from datetime import datetime


def enumerate_tls(target, port):

    result = {
        "tls_version": "Unknown",
        "issuer": "Unknown",
        "subject": "Unknown",
        "expires": "Unknown",
        "days_remaining": None,
        "valid": False
    }

    try:

        context = ssl.create_default_context()

        with socket.create_connection((target, port), timeout=5) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=target
            ) as ssock:

                cert = ssock.getpeercert()

                result["tls_version"] = ssock.version()

                issuer = dict(x[0] for x in cert["issuer"])
                subject = dict(x[0] for x in cert["subject"])

                result["issuer"] = issuer.get(
                    "organizationName",
                    "Unknown"
                )

                result["subject"] = subject.get(
                    "commonName",
                    "Unknown"
                )

                expires = cert["notAfter"]

                result["expires"] = expires

                expire_date = datetime.strptime(
                    expires,
                    "%b %d %H:%M:%S %Y %Z"
                )

                remaining = (
                    expire_date - datetime.utcnow()
                ).days

                result["days_remaining"] = remaining
                result["valid"] = remaining > 0

    except Exception:
        pass

    return result