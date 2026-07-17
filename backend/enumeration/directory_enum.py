import requests
import urllib3

# SSL warning hide
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMMON_PATHS = [
    "/robots.txt",
    "/sitemap.xml",
    "/favicon.ico",
    "/login",
    "/admin",
    "/administrator",
    "/dashboard",
    "/api",
    "/graphql",
    "/uploads",
    "/backup",
    "/config",
    "/phpinfo.php",
    "/server-status",
    "/wp-admin",
    "/wp-login.php",
    "/.git",
    "/.env",
]


def enumerate_directories(target, port):
    protocol = "https" if port == 443 else "http"
    base_url = f"{protocol}://{target}"
    results = []

    for path in COMMON_PATHS:
        url = base_url + path

        try:
            response = requests.get(
                url,
                timeout=3,
                verify=False,
                allow_redirects=False,
                headers={
                    "User-Agent": "Mozilla/5.0 AegisAI"
                }
            )

            print(path, response.status_code)

            # 🔥 FIX: 301/302 spam removed. Reporting only genuinely accessible or restricted resources.
            if response.status_code in [200, 401, 403]:
                results.append({
                    "path": path,
                    "status": response.status_code,
                    "redirect": response.headers.get("Location", "None")
                })

        except requests.RequestException:
            continue

    return results