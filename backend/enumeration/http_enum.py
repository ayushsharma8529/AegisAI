import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def enumerate_http(target, port):

    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{target}"

    result = {
        "title": "Unknown",
        "server": "Unknown",
        "powered_by": "Unknown",
        "redirect": None,
        "cookies": [],
        "security_headers": {}
    }

    try:

        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
            verify=False
        )

        # Title
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.title:
            result["title"] = soup.title.text.strip()

        # Server Header
        result["server"] = response.headers.get(
            "Server",
            "Unknown"
        )

        # X-Powered-By
        result["powered_by"] = response.headers.get(
            "X-Powered-By",
            "Unknown"
        )

        # Redirect
        if "Location" in response.headers:
            result["redirect"] = response.headers["Location"]

        # Cookies
        result["cookies"] = list(response.cookies.keys())

        # Security Headers
        headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]

        for h in headers:
            result["security_headers"][h] = h in response.headers

    except Exception:
        pass

    return result