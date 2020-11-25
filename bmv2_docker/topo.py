import os
from mininet.net import  Containernet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Docker
from p4_mininet import P4Switch, P4Host
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=False, default='simple_switch' )
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=2)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)

args = parser.parse_args()

def main():
    net = Containernet(host = P4Host, controller = None)

    switch1 = net.addSwitch('s1', sw_path = args.behavioral_exe, json_path = args.json, thrift_port = args.thrift_port, cls = P4Switch, pcap_dump = args.pcap_dump)

    host1 = net.addHost('h1', mac = '00:00:00:00:00:01', ip= '10.0.0.1')
    host2 = net.addDocker('h2', mac = '00:00:00:00:00:02',  ip= '10.0.0.2', dimage="ubuntu:trusty")

    net.addLink(host1, switch1, port1 = 0, port2 = 1)
    net.addLink(host2, switch1, port1 = 0, port2 = 2)
    net.start()

    h1,h2=net.get('h1','h2')
    h1.cmd("arp -s 10.0.0.2 00:00:00:00:00:02")
    h1.cmd("ethtool -K eth0 tx off rx off")
    h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01")
    h2.cmd("ethtool -K h2-eth0 tx off rx off")

    sleep(1)
    print('\033[0;32m'),
    print('\033[0m')

    CLI(net)
    try:
        net.stop()

    except:
        print('\033[0;31m'),
        print('Stop error! Trying sudo mn -c')
        print('\033[0m')
        os.system('sudo mn -c')
        print('\033[0;32m'),
        print ('Stop successfully!')
        print('\033[0m')

if __name__ == '__main__':
    setLogLevel('info')
    main()
