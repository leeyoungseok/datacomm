from scapy.all import sniff, IP, UDP, DNS

def parse_packet(packet):
    if IP in packet and UDP in packet:
        ip_layer = packet[IP]
        udp_layer = packet[UDP]
        
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        src_port = udp_layer.sport
        dst_port = udp_layer.dport
        protocol = ip_layer.proto
        if packet.haslayer(DNS):
            dns_packet = packet[DNS]
            dns_payload = dns_packet.summary()
        
        print(f'Source IP: {src_ip}, Source Port: {src_port}')
        print(f'Destination IP: {dst_ip}, Destination Port: {dst_port}')
        print(f'IP protocol: {protocol}')
        #print(f'Payload: {bytes(udp_layer.payload)}\n')
        print(f'DNS Payload: {dns_payload}\n')

def main():
    # Sniff UDP packets
    print("Starting packet sniffing...")
    sniff(filter="udp port 53", prn=parse_packet, count=5)

if __name__ == "__main__":
    main()
