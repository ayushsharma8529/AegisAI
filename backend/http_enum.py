import requests
from bs4 import BeautifulSoup


def enumerate_http(target, port):

    protocol = "https" if port == 443 else "http"

    url = f"{protocol}://{target}"

    try:

        response = requests.get(
            url,
            timeout=3,
            verify=False
        )

        soup = BeautifulSoup(response.text, "html.parser")

        title = "Unknown"

        if soup.title:
            title = soup.title.string.strip()

        return {
            "status_code": response.status_code,
            "server": response.headers.get("Server", "Unknown"),
            "powered_by": response.headers.get("X-Powered-By", "Unknown"),
            "content_type": response.headers.get("Content-Type", "Unknown"),
            "title": title
        }

    except Exception:

        return {
            "status_code": "Unknown",
            "server": "Unknown",
            "powered_by": "Unknown",
            "content_type": "Unknown",
            "title": "Unknown"
        }