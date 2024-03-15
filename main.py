import os
from modules.cve_check import check_cve
from modules.host_scan import scan_host
from modules.network_scan import scan
from modules.wireless_scan import wireless_network_scan

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear_screen()
    print("Welcome to Vulnerability Assessment Tool\n")
    print("1. CVE Check")
    print("2. Host Scan")
    print("3. Network Scan")
    print("4. Wireless Network Scan")
    print("5. Exit\n")

def cve_check():
    clear_screen()
    print("=== CVE Check ===")
    print("Please enter a CVE ID in the format 'CVE-Year-Number', e.g., 'CVE-2021-12345'")
    cve_id = input("Enter CVE ID to check for vulnerabilities: ")    
    check_cve(cve_id)
    input("\nPress Enter to return to the main menu...")

def host_scan():
    clear_screen()
    print("=== Host Scan ===")
    host = input("Enter the host to scan: ")
    ports_str = input("Enter the ports to scan (comma-separated): ")
    ports = [int(port) for port in ports_str.split(",")]
    scan_host(host, ports)
    input("\nPress Enter to return to the main menu...")

def network_scan():
    clear_screen()
    print("=== Network Scan ===")
    target = input("Enter target IP or hostname to scan: ")
    scan(target)
    input("\nPress Enter to return to the main menu...")

def wireless_scan():
    clear_screen()
    print("=== Wireless Network Scan ===")
    interface = input("Enter the wireless interface to scan (e.g., 'wlan0', 'en0', 'eth0') or press ENTER to scan all interfaces: ")
    wireless_network_scan(interface)
    input("\nPress Enter to return to the main menu...")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            cve_check()
        elif choice == '2':
            host_scan()
        elif choice == '3':
            network_scan()
        elif choice == '4':
            wireless_scan()
        elif choice == '5':
            clear_screen()
            print("Exiting. Goodbye!")
            break
        else:
            clear_screen()
            print("Invalid choice. Please enter a valid option.\n")

if __name__ == "__main__":
    main()
