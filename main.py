from scapy.all import *
import netifaces
import curses
import os
from modules.cve_check import check_cve
from modules.host_scan import scan_host
from modules.network_scan import scan
from modules.wireless_scan import wireless_network_scan

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Vulnerability Assessment Tool\n")
    stdscr.addstr(2, 0, "1. CVE Check")
    stdscr.addstr(3, 0, "2. Network Scan")
    stdscr.addstr(4, 0, "3. Host Scan")
    stdscr.addstr(5, 0, "4. Wireless Network Scan")
    stdscr.addstr(6, 0, "5. Exit\n")
    stdscr.refresh()

def cve_check(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "=== CVE Check ===")
    stdscr.addstr(2, 0, "Please enter a CVE ID in the format 'CVE-Year-Number', e.g., 'CVE-2021-12345'")
    stdscr.addstr(3, 0, "Enter CVE ID to check for vulnerabilities: ")
    stdscr.refresh()
    cve_id = get_input(stdscr, 3, len("Enter CVE ID to check for vulnerabilities: ") + 1)  
    check_cve(cve_id, stdscr)
    stdscr.addstr(curses.LINES - 1, 0, "Press Enter to return to the main menu...")
    stdscr.refresh()
    stdscr.getch()

def host_scan(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "=== Host Scan ===")
    stdscr.addstr(2, 0, "Enter the host to scan: ")
    stdscr.refresh()
    host = get_input(stdscr, 3, 0)
    stdscr.addstr(4, 0, "Enter the ports to scan (comma-separated): ")
    stdscr.refresh()
    ports_str = get_input(stdscr, 5, 0)
    ports = [int(port) for port in ports_str.split(",")]
    scan_host(stdscr, host, ports)
    stdscr.addstr(curses.LINES - 1, 0, "Press Enter to return to the main menu...")
    stdscr.refresh()
    stdscr.getch()

def network_scan(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "=== Network Scan ===")
    stdscr.addstr(2, 0, "Enter target IP or hostname to scan: ")
    stdscr.refresh()
    target = get_input(stdscr, 3, 0)
    scan(stdscr, target)
    stdscr.addstr(curses.LINES - 1, 0, "Press Enter to return to the main menu...")
    stdscr.refresh()
    stdscr.getch()

def list_network_interfaces():
    interfaces = netifaces.interfaces()
    return interfaces

def select_interface(stdscr):
    interfaces = list_network_interfaces()
    stdscr.clear()
    stdscr.addstr(0, 0, "=== Select Interface ===")
    stdscr.addstr(2, 0, "Available interfaces:")
    for i, interface in enumerate(interfaces, start=1):
        stdscr.addstr(i + 2, 0, f"{i}. {interface}")
    
    input_str = ""  # Store the current input string

    while True:
        try:
            stdscr.addstr(len(interfaces) + 4, 0, " " * (curses.COLS - 1))  
            stdscr.addstr(len(interfaces) + 4, 0, f"Enter the number of the interface to scan: {input_str}")  
            stdscr.refresh()
            ch = stdscr.getch()
            if ch == curses.KEY_ENTER or ch == 10: 
                choice = int(input_str)
                if 1 <= choice <= len(interfaces):
                    return interfaces[choice - 1]
                else:
                    stdscr.addstr(len(interfaces) + 5, 0, "Invalid choice. Enter the number of the interface to scan: ")
                    stdscr.refresh()
            elif ch == curses.KEY_BACKSPACE or ch == 127:  
                input_str = input_str[:-1]  
            elif 48 <= ch <= 57:  
                input_str += chr(ch)  
            else:
                pass  
        except ValueError:
            stdscr.addstr(len(interfaces) + 5, 0, "Invalid choice. Enter the number of the interface to scan: ")
            stdscr.refresh()
        except curses.error:
            pass

def wireless_scan(stdscr):
    interface = select_interface(stdscr)
    if interface:
        wireless_network_scan(interface, stdscr)
        stdscr.addstr(curses.LINES - 1, 0, "Press Enter to return to the main menu...")
        stdscr.refresh()
        stdscr.getch()

def get_input(stdscr, row, col):
    curses.echo()  
    input_str = stdscr.getstr(row, col).decode('utf-8')
    curses.noecho()  
    return input_str

def main(stdscr):
    while True:
        display_menu(stdscr)
        choice = stdscr.getch()

        if choice == ord('1'):
            cve_check(stdscr)
        elif choice == ord('2'):
            network_scan(stdscr)
        elif choice == ord('3'):
            host_scan(stdscr)
        elif choice == ord('4'):
            wireless_scan(stdscr)
        elif choice == ord('5'):
            clear_screen()
            stdscr.addstr(7, 0, "Exiting. Goodbye!")
            stdscr.refresh()
            stdscr.getch()
            break
        else:
            stdscr.clear()
            stdscr.addstr(7, 0, "Invalid choice. Please enter a valid option.")
            stdscr.refresh()
            stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)