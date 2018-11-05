import os
import sys
from PcapToFlows.pcap_to_flows import sort_flows


def main():
    """Main."""
    for file in os.listdir('data'):
        if os.path.isdir(file):
            continue
        file_comps = os.path.splitext(file)
        if file_comps[1] != '.pcapng':
            continue
        output_dir = 'data/' + file_comps[0]
        with open('data/' + file, 'rb') as pcap:
            sort_flows(pcap, '192.168.1.67', output_dir)


if __name__ == '__main__':
    main()
