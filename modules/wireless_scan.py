from scapy.all import *
import curses

def wireless_network_scan(interface, stdscr):
    try:
        stdscr.scrollok(True) 
        stdscr.addstr(f"\nScanning for IPv6 networks on interface {interface}...\n")
        stdscr.refresh()

        networks = set()

        def packet_handler(packet):
            if IPv6 in packet:
                src = packet[IPv6].src
                dst = packet[IPv6].dst
                networks.add(src)
                networks.add(dst)
                try:
                    stdscr.addstr("Received packet: " + packet.summary() + "\n")
                except curses.error:
                    print("Error: Couldn't display packet information due to terminal limitations.")
                stdscr.refresh()

        sniff(iface=interface, prn=packet_handler, timeout=10)

        try:
            stdscr.addstr("\nIPv6 Networks Found:\n")
            for network in networks:
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