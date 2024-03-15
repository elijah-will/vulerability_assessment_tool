from scapy.all import *

def wireless_network_scan(interface):
    print(f"Scanning for IPv6 networks on interface {interface}...\n")
    networks = set()

    def packet_handler(packet):
        if IPv6 in packet:
            src = packet[IPv6].src
            dst = packet[IPv6].dst
            networks.add(src)
            networks.add(dst)
            print("Received packet:", packet.summary())  # Debug print to see received packets

    sniff(iface=interface, prn=packet_handler, timeout=10)

    print("IPv6 Networks Found:")
    for network in networks:
        print(network)

