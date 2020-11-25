## 拓扑

```
 +-------------------BMV2-------------------+
 |                                          |
 |                                          |
h1(host)                             h2(container)
```

## P4 build

```bash
make build
```

## Run topo
```bash
make topo
```

## Add table entries
```bash
make table
```

## Test
```
# show docker container
sudo docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
4c8b0a5dd1cd        ubuntu:trusty       "/bin/bash"         5 minutes ago       Up 5 minutes                            mn.h2


# mininet CLI
containernet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.322 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=1.53 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=1.66 ms


# docker container
sudo docker exec -it mn.h2 /bin/bash
apt-get update
apt-get install iperf


# docker container
iperf -s -i 1

# mininet CLI
containernet> h1 iperf -c 10.0.0.2 -i 1
------------------------------------------------------------
Client connecting to 10.0.0.2, TCP port 5001
TCP window size:  187 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.1 port 49126 connected with 10.0.0.2 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  19.9 MBytes   167 Mbits/sec
[  3]  1.0- 2.0 sec  18.8 MBytes   157 Mbits/sec
[  3]  2.0- 3.0 sec  18.6 MBytes   156 Mbits/sec
[  3]  3.0- 4.0 sec  19.6 MBytes   165 Mbits/sec
[  3]  4.0- 5.0 sec  18.6 MBytes   156 Mbits/sec
[  3]  5.0- 6.0 sec  18.6 MBytes   156 Mbits/sec
[  3]  6.0- 7.0 sec  18.6 MBytes   156 Mbits/sec
[  3]  7.0- 8.0 sec  18.6 MBytes   156 Mbits/sec
[  3]  8.0- 9.0 sec  18.8 MBytes   157 Mbits/sec
[  3]  9.0-10.0 sec  18.8 MBytes   157 Mbits/sec
[  3]  0.0-10.0 sec   189 MBytes   158 Mbits/sec


# docker container
iperf -s -i 1 -u

# mininet CLI
containernet> h1 iperf -c 10.0.0.2 -i 1 -u
------------------------------------------------------------
Client connecting to 10.0.0.2, UDP port 5001
Sending 1470 byte datagrams, IPG target: 11215.21 us (kalman adjust)
UDP buffer size:  208 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.1 port 43837 connected with 10.0.0.2 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec   131 KBytes  1.07 Mbits/sec
[  3]  1.0- 2.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  2.0- 3.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  3.0- 4.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  4.0- 5.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  5.0- 6.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  6.0- 7.0 sec   129 KBytes  1.06 Mbits/sec
[  3]  7.0- 8.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  8.0- 9.0 sec   128 KBytes  1.05 Mbits/sec
[  3]  0.0-10.0 sec  1.25 MBytes  1.05 Mbits/sec
[  3] Sent 892 datagrams
```
