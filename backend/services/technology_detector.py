def detect_technology(headers, banner):

    tech = {
        "server": "Unknown",
        "language": "Unknown",
        "framework": "Unknown",
        "cms": "Unknown",
        "frontend": "Unknown"
    }

    text = f"{headers} {banner}".lower()

    # --- Web Server ---
    if "nginx" in text:
        tech["server"] = "Nginx"

    elif "apache" in text:
        tech["server"] = "Apache"

    elif "iis" in text:
        tech["server"] = "Microsoft IIS"

    elif "gws" in text:
        tech["server"] = "Google Web Server"

    elif "proxygen" in text:
        tech["server"] = "Proxygen"

    elif "cloudflare" in text:
        tech["server"] = "Cloudflare"

    elif "openresty" in text:
        tech["server"] = "OpenResty"

    elif "caddy" in text:
        tech["server"] = "Caddy"

    elif "lighttpd" in text:
        tech["server"] = "Lighttpd"

    elif "tomcat" in text:
        tech["server"] = "Apache Tomcat"

    elif "gunicorn" in text:
        tech["server"] = "Gunicorn"

    elif "uvicorn" in text:
        tech["server"] = "Uvicorn"

    # --- Languages ---
    if "php" in text:
        tech["language"] = "PHP"

    elif "asp.net" in text:
        tech["language"] = "ASP.NET"

    elif "express" in text:
        tech["language"] = "Node.js"

    elif "python" in text:
        tech["language"] = "Python"

    elif "java" in text:
        tech["language"] = "Java"

    elif "ruby" in text:
        tech["language"] = "Ruby"

    elif "go" in text:
        tech["language"] = "Go"

    # --- Framework ---
    if "laravel" in text:
        tech["framework"] = "Laravel"

    elif "django" in text:
        tech["framework"] = "Django"

    elif "flask" in text:
        tech["framework"] = "Flask"

    elif "spring" in text:
        tech["framework"] = "Spring"

    elif "fastapi" in text:
        tech["framework"] = "FastAPI"

    elif "next.js" in text:
        tech["framework"] = "Next.js"

    elif "nextjs" in text:
        tech["framework"] = "Next.js"

    elif "express" in text:
        tech["framework"] = "Express"

    elif "rails" in text:
        tech["framework"] = "Ruby on Rails"

    elif "bootstrap" in text:
        tech["framework"] = "Bootstrap"

    # --- CMS ---
    if "wordpress" in text:
        tech["cms"] = "WordPress"

    elif "drupal" in text:
        tech["cms"] = "Drupal"

    elif "joomla" in text:
        tech["cms"] = "Joomla"

    elif "shopify" in text:
        tech["cms"] = "Shopify"

    elif "wix" in text:
        tech["cms"] = "Wix"

    elif "squarespace" in text:
        tech["cms"] = "Squarespace"

    # --- Frontend ---
    if "react" in text:
        tech["frontend"] = "React"

    elif "vue" in text:
        tech["frontend"] = "Vue"

    elif "angular" in text:
        tech["frontend"] = "Angular"

    elif "jquery" in text:
        tech["frontend"] = "jQuery"

    elif "tailwind" in text:
        tech["frontend"] = "Tailwind CSS"

    elif "bootstrap" in text:
        tech["frontend"] = "Bootstrap"

    return tech