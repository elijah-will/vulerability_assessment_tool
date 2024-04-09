from scapy.all import *
import curses

def wireless_network_scan(interface, stdscr):
    try:
        stdscr.scrollok(True) 
        stdscr.addstr(f"\nScanning for IPv4 and IPv6 networks on interface {interface}...\n")
        stdscr.refresh()

        ipv4_networks = set()
        ipv6_networks = set()

        def packet_handler(packet):
            if IP in packet:
                src = packet[IP].src
                dst = packet[IP].dst
                ipv4_networks.add(src)
                ipv4_networks.add(dst)
            elif IPv6 in packet:
                src = packet[IPv6].src
                dst = packet[IPv6].dst
                ipv6_networks.add(src)
                ipv6_networks.add(dst)
            
            try:
                stdscr.addstr("Received packet: " + packet.summary() + "\n")
            except curses.error:
                print("Error: Couldn't display packet information due to terminal limitations.")
            stdscr.refresh()

        sniff(iface=interface, prn=packet_handler, timeout=10)

        try:
            stdscr.addstr("\nIPv4 Networks Found:\n")
            for network in ipv4_networks:
                try:
                    stdscr.addstr(network + "\n")
                except curses.error as e:
                    if e.args[0] == curses.ERR:
                        print("Error: Couldn't display network information due to terminal limitations.")
                        return  # End the function
                    else:
                        raise  
            stdscr.addstr("\nIPv6 Networks Found:\n")
            for network in ipv6_networks:
                try:
                    stdscr.addstr(network + "\n")
                except curses.error as e:
                    if e.args[0] == curses.ERR:
                        print("Error: Couldn't display network information due to terminal limitations.")
                        return  # End the function
                    else:
                        raise  
        except curses.error as e:
            if e.args[0] == curses.ERR:
                print("Error: Couldn't display network information due to terminal limitations.")
            else:
                raise  
        stdscr.refresh()

    except OSError:
        stdscr.addstr("Error: Interface not found.\n")
        stdscr.refresh()
    except Scapy_Exception as e:
        print(f"Error: {e}")