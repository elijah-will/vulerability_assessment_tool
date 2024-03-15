import nmap

def scan(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-Pn -sV')
    
    print("Scanning target:", target)
    for host in scanner.all_hosts():
        print("Host:", host)
        for proto in scanner[host].all_protocols():
            print("Protocol:", proto)
            ports = scanner[host][proto].keys()
            
            for port in ports:
                state = scanner[host][proto][port]['state']
                service = scanner[host][proto][port]['name']
                product = scanner[host][proto][port]['product']
                version = scanner[host][proto][port]['version']
                
                print("Port:", port, "State:", state, "Service:", service)
                if product:
                    print("    Product:", product)
                if version:
                    print("    Version:", version)

