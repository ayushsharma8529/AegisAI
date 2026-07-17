import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def enumerate_http(target, port):

    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{target}"

    # Step 1 — Result dictionary expand kiya gaya
    result = {
        "title": "Unknown",
        "server": "Unknown",
        "powered_by": "Unknown",
        "redirect": None,
        "cookies": [],
        "security_headers": {},

        "content_type": "Unknown",
        "content_length": "Unknown",
        "cache_control": "Unknown",
        "etag": "Unknown",
        "permissions_policy": "Unknown",
        "x_generator": "Unknown",
        "via": "Unknown"
    }

    try:
        # Step 4 — User-Agent custom headers ke sath request send ki
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
            verify=False,
            headers={
                "User-Agent": "AegisAI Security Scanner/1.0"
            }
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

        # Step 2 — Response headers se nayi values extract ki gayi
        result["content_type"] = response.headers.get(
            "Content-Type",
            "Unknown"
        )
        result["content_length"] = response.headers.get(
            "Content-Length",
            "Unknown"
        )
        result["cache_control"] = response.headers.get(
            "Cache-Control",
            "Unknown"
        )
        result["etag"] = response.headers.get(
            "ETag",
            "Unknown"
        )
        result["permissions_policy"] = response.headers.get(
            "Permissions-Policy",
            "Unknown"
        )
        result["x_generator"] = response.headers.get(
            "X-Generator",
            "Unknown"
        )
        result["via"] = response.headers.get(
            "Via",
            "Unknown"
        )

        # Redirect
        if "Location" in response.headers:
            result["redirect"] = response.headers["Location"]

        # Cookies
        result["cookies"] = list(response.cookies.keys())

        # Step 3 — Security Headers list improve ki gayi (Permissions-Policy added)
        headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        for h in headers:
            result["security_headers"][h] = h in response.headers

    except Exception:
        pass

    return result