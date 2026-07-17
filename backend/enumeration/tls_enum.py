import socket
import ssl
from datetime import datetime

def enumerate_tls(hostname, port=443):
    result = {
        "tls_version": "Unknown",
        "issuer": "Unknown",
        "subject": "Unknown",
        "expires": "Unknown",
        "days_remaining": "Unknown",
        "certificate_status": "Invalid" # Default or fallback status
    }
    
    context = ssl.create_default_context()
    # Agar self-signed certificates ya expired certs ko bhi connect karne dena hai 
    # debugging/scanning ke liye, toh aap in lines ko uncomment kar sakte hain:
    # context.check_hostname = False
    # context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                
                # Connection successful and verified by default context rules
                result["certificate_status"] = "Valid"
                
                # Protocol Version Extraction
                if cipher:
                    result["tls_version"] = cipher[1]
                
                # Certificate Details Parsing
                if cert:
                    # Issuer Parsing
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    result["issuer"] = issuer.get('organizationName', issuer.get('commonName', 'Unknown'))
                    
                    # Subject Parsing
                    subject = dict(x[0] for x in cert.get('subject', []))
                    result["subject"] = subject.get('commonName', 'Unknown')
                    
                    # Expiration Extraction
                    not_after_str = cert.get('notAfter')
                    if not_after_str:
                        result["expires"] = not_after_str
                        
                        # Remaining Days Calculation
                        try:
                            expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                            remaining = expiry_date - datetime.utcnow()
                            result["days_remaining"] = max(0, remaining.days)
                            
                            # Additional safety check: Expiry date cross ho chuki hai toh invalid handle karein
                            if remaining.days < 0:
                                result["certificate_status"] = "Invalid (Expired)"
                        except Exception:
                            pass

    except ssl.SSLError as ssl_err:
        # SSL Verification failure triggers explicit Invalid status
        result["certificate_status"] = "Invalid"
        # Optional: dynamic message structure context ke liye save kar sakte hain
        # result["error_details"] = str(ssl_err)
    except Exception as e:
        # Generic connection or parsing fallback
        result["certificate_status"] = "Invalid"
        
    return result