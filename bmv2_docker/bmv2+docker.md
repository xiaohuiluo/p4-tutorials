## 拓扑

```
 +-------------------BMV2-------------------+
 |                                          |
 |                                          |
h1(h1-eth0)                             h2(h2-eth0)
```



## docker容器

1. 创建2个docker容器

   ```bash
   sudo docker run -itd --name=ubuntu1 --network=none ubuntu:trusty
   sudo docker run -itd --name=ubuntu2 --network=none ubuntu:trusty
   ```



2. 获取容器pid

   ```bash
   PID1=$(sudo docker inspect -f '{{.State.Pid}}' ubuntu1)
   PID2=$(sudo docker inspect -f '{{.State.Pid}}' ubuntu2)
   ```

3. docker容器进程namespace恢复到主机

   ```bash
   sudo mkdir -p /var/run/netns
   sudo ln -s /proc/$PID1/ns/net /var/run/netns/$PID1
   sudo ln -s /proc/$PID2/ns/net /var/run/netns/$PID2
   # 查看netns
   sudo ip netns list
   ```

4. docker容器添加veth peer

   ```bash
   sudo ip link add h1-eth0 type veth peer name s1-eth0
   sudo ip link set h1-eth0 netns $PID1
   sudo ip link set s1-eth0 up
   sudo ip netns exec $PID1 ifconfig h1-eth0 hw ether 00:00:00:00:00:01
   sudo ip netns exec $PID1 ip link set h1-eth0 up
   sudo ip netns exec $PID1 ip addr add 10.0.0.1/24 dev h1-eth0
   sudo ip netns exec $PID1 arp -s 10.0.0.2 00:00:00:00:00:02

   sudo ip link add h2-eth0 type veth peer name s1-eth1
   sudo ip link set h2-eth0 netns $PID2
   sudo ip link set s1-eth1 up
   sudo ip netns exec $PID2 ifconfig h2-eth0 hw ether 00:00:00:00:00:02
   sudo ip netns exec $PID2 ip link set h2-eth0 up
   sudo ip netns exec $PID2 ip addr add 10.0.0.2/24 dev h2-eth0
   sudo ip netns exec $PID2 arp -s 10.0.0.1 00:00:00:00:00:01
   ```

## BMV2

1. 启动bmv2交换机s1

   ```bash
   sudo simple_switch -i 1@s1-eth0 -i 2@s1-eth1 build/bmv2.json
   ```

2. 流表

   ```bash
   sudo simple_switch_CLI --thrift-port=9090

   table_add ipv4_lpm ipv4_forward 10.0.0.1/32 => 1
   table_add ipv4_lpm ipv4_forward 10.0.0.2/32 => 2
   ```

## Test

```bash
sudo docker exec -it ubuntu1 /bin/bash
    # show ip
    ip a

    # ping h2
    ping 10.0.0.2

sudo docker exec -it ubuntu2 /bin/bash
    # show ip
    ip a

    # ping h1
    ping 10.0.0.1
```

## clean
```bash
sudo docker stop ubuntu1 ubuntu2
sudo docker rm ubuntu1 ubuntu2
sudo ip link delete s1-eth1
sudo ip link delete s1-eth0
sudo rm -rf /var/run/netns
```
