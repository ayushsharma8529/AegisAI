import requests


def detect_http_methods(target, port):

    protocol = "https" if port == 443 else "http"

    url = f"{protocol}://{target}"

    try:
        response = requests.options(
            url,
            timeout=5,
            verify=False,
            allow_redirects=False
        )
        print(response.status_code)
        print(response.headers)

        allow = response.headers.get("Allow", "")

        methods = [
            method.strip()
            for method in allow.split(",")
            if method.strip()
        ]

        return {
            "allowed_methods": methods
        }

    except Exception:

        return {
            "allowed_methods": []
        }