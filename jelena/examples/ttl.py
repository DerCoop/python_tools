#!/usr/bin/env python

import scapy.layers.l2
import scapy.layers.inet
from scapy.all import wrpcap
import sys


def generatePCAP(filename1='out1.pcap', filename2='out2.pcap'):
    # first
    frames = []
    ethernet_layer = scapy.layers.l2.Ether()
    ip_layer = scapy.layers.inet.IP()
    ip_layer.ttl = 63
    packet = ethernet_layer/ip_layer
    packet.time = 0
    frames.append(packet)

    wrpcap(filename1, frames)

    # second
    frames = []
    ethernet_layer = scapy.layers.l2.Ether()
    ip_layer = scapy.layers.inet.IP()
    packet = ethernet_layer/ip_layer
    packet.time = 0
    frames.append(packet)

    wrpcap(filename2, frames)

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 2:
        f1 = sys.argv[1]
        f2 = sys.argv[2]
    else:
        f1 = 'out1.pcap'
        f2 = 'out2.pcap'
    generatePCAP(f1, f2)
