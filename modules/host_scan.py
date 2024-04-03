import socket
import subprocess
import curses

def check_vulnerabilities(host, port):
    vulnerabilities = []

    try:
        if not 0 <= port <= 65535:
            raise ValueError(f"Invalid port number: {port}. Port number must be between 0 and 65535.")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))

        if result == 0:
            vulnerabilities.append(f"Port {port}: Open")
            if port == 22:
                vulnerabilities.append("Potential SSH vulnerability")
            elif port == 80:
                vulnerabilities.append("Potential HTTP vulnerability")
            elif port == 443:
                vulnerabilities.append("Potential HTTPS vulnerability")
        else:
            vulnerabilities.append(f"Port {port}: Closed or not in use")

        sock.close()
    except ValueError as ve:
        vulnerabilities.append(str(ve))
    except socket.timeout:
        vulnerabilities.append(f"Timeout scanning port {port} on host {host}")
    except socket.error as se:
        vulnerabilities.append(f"Socket error scanning port {port} on host {host}: {se}")
    except Exception as e:
        vulnerabilities.append(f"Error scanning port {port}: {e}")

    return vulnerabilities

def nmap_scan(host):
    try:
        result = subprocess.run(['nmap', '-Pn', '-p-', host], capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, ' '.join(result.args))
        return result.stdout
    except FileNotFoundError:
        return "Nmap command not found. Please install Nmap."
    except subprocess.CalledProcessError as cpe:
        return f"Nmap scan failed with return code {cpe.returncode}: {cpe.stderr}"
    except Exception as e:
        return f"Error scanning host {host} with Nmap: {e}"

def scan_host(stdscr, host, ports):
    stdscr.scrollok(True) 
    stdscr.clear()
    stdscr.addstr(0, 0, f"Scanning host {host}...")
    stdscr.refresh()

    y = 2
    for port in ports:
        vulnerabilities = check_vulnerabilities(host, port)
        for vulnerability in vulnerabilities:
            stdscr.addstr(y, 0, vulnerability)
            y += 1

    stdscr.addstr(y, 0, "Running Nmap scan for additional vulnerabilities...")
    stdscr.refresh()

    try:
        nmap_result = nmap_scan(host)
        nmap_lines = nmap_result.split('\n')
        num_lines = min(len(nmap_lines), curses.LINES - y - 2)  
        for i in range(num_lines):
            stdscr.addstr(y + i + 1, 0, nmap_lines[i])
    except Exception as e:
        stdscr.addstr(y + 1, 0, f"Error: {e}")

    stdscr.refresh()
    
    curses.napms(3000) 
    curses.endwin()  

