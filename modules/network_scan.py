import curses
import nmap

def scan(stdscr, target):
    try:
        stdscr.scrollok(True)  
        scanner = nmap.PortScanner()
        scanner.scan(target, arguments='-Pn -sV')
        
        stdscr.clear()
        stdscr.addstr(0, 0, "Scanning target: " + target)
        stdscr.refresh()
        
        y = 2
        for host in scanner.all_hosts():
            stdscr.addstr(y, 0, "Host: " + host)
            y += 1
            for proto in scanner[host].all_protocols():
                stdscr.addstr(y, 0, "  Protocol: " + proto)
                y += 1
                ports = scanner[host][proto].keys()
                
                for port in ports:
                    state = scanner[host][proto][port]['state']
                    service = scanner[host][proto][port]['name']
                    product = scanner[host][proto][port]['product']
                    version = scanner[host][proto][port]['version']
                    
                    stdscr.addstr(y, 0, "-" * curses.COLS)  
                    y += 1
                    stdscr.addstr(y, 0, f"    Port: {port}, State: {state}, Service: {service}")
                    y += 1
                    if product:
                        stdscr.addstr(y, 4, "Product: " + product)
                        y += 1
                    if version:
                        stdscr.addstr(y, 4, "Version: " + version)
                        y += 1
                stdscr.addstr(y, 0, "-" * curses.COLS)  
                y += 1
        
        stdscr.refresh()
    except nmap.PortScannerError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, "Error: " + str(e))
        stdscr.refresh()

