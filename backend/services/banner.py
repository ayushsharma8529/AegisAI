import ssl
import socket


def grab_banner(target, port):
    try:

        if port == 80:

            sock = socket.create_connection((target, port), timeout=2)

            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                "User-Agent: AegisAI/1.0\r\n"
                "Connection: close\r\n\r\n"
            )

            sock.sendall(request.encode())

            banner = receive(sock)

            sock.close()

            return banner


        elif port == 443:

            context = ssl.create_default_context()

            raw = socket.create_connection((target, port), timeout=2)

            sock = context.wrap_socket(raw, server_hostname=target)

            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                "User-Agent: AegisAI/1.0\r\n"
                "Connection: close\r\n\r\n"
            )

            sock.sendall(request.encode())

            banner = receive(sock)

            sock.close()

            return banner


        else:

            sock = socket.create_connection((target, port), timeout=2)

            banner = receive(sock)

            sock.close()

            return banner

    except:
        return "No banner"


def receive(sock):

    data = b""

    while True:

        try:

            chunk = sock.recv(4096)

            if not chunk:
                break

            data += chunk

        except:
            break

    text = data.decode(errors="ignore")

    return text[:3000]