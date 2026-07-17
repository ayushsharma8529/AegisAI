def detect_technology(headers, banner):

    tech = {
        "server": "Unknown",
        "language": "Unknown",
        "framework": "Unknown",
        "cms": "Unknown",
        "frontend": "Unknown"
    }

    text = f"{headers} {banner}".lower()

    # Web Server
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

    # Languages

    if "php" in text:
        tech["language"] = "PHP"

    elif "asp.net" in text:
        tech["language"] = "ASP.NET"

    elif "express" in text:
        tech["language"] = "Node.js"

    # Framework

    if "laravel" in text:
        tech["framework"] = "Laravel"

    elif "django" in text:
        tech["framework"] = "Django"

    elif "flask" in text:
        tech["framework"] = "Flask"

    elif "spring" in text:
        tech["framework"] = "Spring"

    # CMS

    if "wordpress" in text:
        tech["cms"] = "WordPress"

    elif "drupal" in text:
        tech["cms"] = "Drupal"

    elif "joomla" in text:
        tech["cms"] = "Joomla"

    # Frontend

    if "react" in text:
        tech["frontend"] = "React"

    elif "vue" in text:
        tech["frontend"] = "Vue"

    elif "angular" in text:
        tech["frontend"] = "Angular"

    return tech