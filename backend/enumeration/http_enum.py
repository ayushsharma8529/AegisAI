import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress insecure request warnings (since verify=False is used)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def enumerate_http(target, port):
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{target}"

    # Step 1 — Result dictionary expanded with 'final_url' and placeholder keys
    result = {
        "title": "Unknown",
        "server": "Unknown",
        "powered_by": "Unknown",
        "redirect": None,
        "final_url": url,  # Default to initial url
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
        # Production Fix 1: Changed allow_redirects to True to hit final destination
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True,
            verify=False,
            headers={
                "User-Agent": "AegisAI Security Scanner/1.0"
            }
        )

        # Production Fix 3: Storing the absolute final URL after all redirects
        result["final_url"] = response.url

        # Production Fix 2: Check if redirects happened and preserve the destination path
        if response.history:
            result["redirect"] = response.url
        else:
            result["redirect"] = None

        # Title Parse (from final page content)
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.title:
            result["title"] = soup.title.text.strip()

        # Server Header (from final destination headers)
        result["server"] = response.headers.get("Server", "Unknown")

        # X-Powered-By
        result["powered_by"] = response.headers.get("X-Powered-By", "Unknown")

        # Step 2 — Response headers extraction (Updates fetched from final landing page)
        result["content_type"] = response.headers.get("Content-Type", "Unknown")
        result["content_length"] = response.headers.get("Content-Length", "Unknown")
        result["cache_control"] = response.headers.get("Cache-Control", "Unknown")
        result["etag"] = response.headers.get("ETag", "Unknown")
        result["permissions_policy"] = response.headers.get("Permissions-Policy", "Unknown")
        result["x_generator"] = response.headers.get("X-Generator", "Unknown")
        result["via"] = response.headers.get("Via", "Unknown")

        # Cookies (Aggregated from final state session)
        result["cookies"] = list(response.cookies.keys())

        # Step 3 — Security Headers verification against final response
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