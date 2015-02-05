#!/usr/bin/env python

from scapy.all import *
import sys


def generatePCAP(filename1='out1.pcap', filename2='out2.pcap'):
    # first
    frames = []
    ethernet_layer = Ether()
    ethernet_layer.src = 'aa:bb:cc:dd:ee:ff'
    ip_layer = IP()
    packet = ethernet_layer/ip_layer
    packet.time = 0
    frames.append(packet)

    wrpcap(filename1, frames)

    # second
    frames = []
    ethernet_layer = Ether()
    ethernet_layer.src = 'ff:de:ad:be:ef:ff'
    ip_layer = IP()
    packet = ethernet_layer/ip_layer
    packet.time = 0
    frames.append(packet)

    wrpcap(filename2, frames)
    return 0

if __name__ == '__main__':
    if len(sys.argv) > 2:
        f1 = sys.argv[1]
        f2 = sys.argv[2]
        generatePCAP(f1, f2)
    else:
        generatePCAP()
