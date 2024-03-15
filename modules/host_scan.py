import socket
import subprocess

def check_vulnerabilities(host, port):
    vulnerabilities = []

    try:
        # Attempt to establish a connection to the host and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))

        # Check if the connection was successful (i.e., port is open)
        if result == 0:
            vulnerabilities.append(f"Port {port}: Open")
            # Here you can add additional checks for specific vulnerabilities based on the port
            if port == 22:
                vulnerabilities.append("Potential SSH vulnerability")
            elif port == 80:
                vulnerabilities.append("Potential HTTP vulnerability")
            elif port == 443:
                vulnerabilities.append("Potential HTTPS vulnerability")
            # Add more checks as needed
        else:
            vulnerabilities.append(f"Port {port}: Closed or not in use")

        sock.close()
    except Exception as e:
        vulnerabilities.append(f"Error scanning port {port}: {e}")

    return vulnerabilities

def nmap_scan(host):
    try:
        result = subprocess.run(['nmap', '-Pn', '-p-', host], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error scanning host {host} with Nmap: {e}"

def scan_host(host, ports):
    print(f"Scanning host {host}...")
    for port in ports:
        if not 0 <= port <= 65535:
            print(f"Port {port}: Invalid port number. Port number must be between 0 and 65535.")
            continue

        vulnerabilities = check_vulnerabilities(host, port)
        for vulnerability in vulnerabilities:
            print(vulnerability)

    print("Running Nmap scan for additional vulnerabilities...")
    nmap_result = nmap_scan(host)
    print(nmap_result)
