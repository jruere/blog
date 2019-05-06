Title: B.A.T.M.A.N Internet Sharing
Date: 2016-03-05 11:17
Category: play
Tags: networking, mesh, linux

# Introduction

This time I'll use a BATMAN mesh to share an existing internet connection.

# How About Some Encryption?

Nope. I failed to setup a WPA Ad-Hoc connection for BATMAN. Don't know what's up.

# Components

1. (A) Custom built PC with a Qualcomm Atheros AR9300 WiFi (`wlan0`) and a D-Link DWA-110 USB WiFi (`wlan1`) and a current Arch Linux.
1. (B) Acer Aspire E15 (E5-521-84UV) laptop with a Broadcom BCM43142 WiFi card and a current Arch Linux.

A current Arch has the 4.4.3 kernel.

# Objectives

The currently working setup is like this:

    Internet → AP → client A

    [BATMAN A → BATMAN B](batman.html)

Client A and BATMAN A are `wlan0` and `wlan1`, respectively, on the same host.

Setup a bridge between wlan0 and wlan1. This should allow the DHCP on the AP to assign addresses. Super easy! :D

# Bridging Official instructions

In [Mixing non-B.A.T.M.A.N. systems with batman-adv](https://www.open-mesh.org/projects/batman-adv/wiki/Quick-start-guide#Mixing-non-BATMAN-systems-with-batman-adv), it shows how to do this, and it's super easy!

The instructions are for bridging `eth0` with `wlan0`, which I suspect is much easier than `wlan0` to `wlan1`.
It does one mysterious thing though (I've changed the device to match my setup):

```text
ip link set mtu 1532 dev wlan1
iwconfig wlan1 mode ad-hoc essid my-mesh-network ap 02:12:34:56:78:9A channel 1
```

What is that `... ap 02:12:34:56:78:9A ...` bit for?

It's in previous commands but I ignored it in the past.

`man iwconfig` says:

```text
[...] If the link  is  ad-hoc, set the cell identity of the ad-hoc network.
```

What?

# Bridging

First, I'll change `wlan0` not to use DHCP and check everything works.

```text
$ ip link
[..]
3: wlan0: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DORMANT group default qlen 1000
    link/ether 90:f6:52:17:92:06 brd ff:ff:ff:ff:ff:ff
4: wlan1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1560 qdisc mq master bat0 state UP mode DORMANT group default qlen 1000
    link/ether 00:1b:11:20:dc:2c brd ff:ff:ff:ff:ff:ff
7: bat0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:b3:d9:3b:62:ea brd ff:ff:ff:ff:ff:ff

$ ip addr
[...]
3: wlan0: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 90:f6:52:17:92:06 brd ff:ff:ff:ff:ff:ff
    inet6 2002:b5ab:1a2a:1:92f6:52ff:fe17:9206/64 scope global mngtmpaddr dynamic 
       valid_lft 278sec preferred_lft 98sec
    inet6 fe80::92f6:52ff:fe17:9206/64 scope link 
       valid_lft forever preferred_lft forever
4: wlan1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1560 qdisc mq master bat0 state UP group default qlen 1000
    link/ether 00:1b:11:20:dc:2c brd ff:ff:ff:ff:ff:ff
    inet6 fe80::21b:11ff:fe20:dc2c/64 scope link 
       valid_lft forever preferred_lft forever
7: bat0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether d2:b3:d9:3b:62:ea brd ff:ff:ff:ff:ff:ff
```

If we ignore the IPv6 address on wlan0, it looks correct. I'm using a bigger MTU as BATMAN complains otherwise and I'm a generous man.

I'll call the bridge `bat-bridge`.

```text
$ sudo ip link set dev wlan0 master bat-bridge
RTNETLINK answers: Operation not supported
$ sudo ip link set dev bat0 master bat-bridge
$ sudo ip link set up dev wlan0
$ sudo ip link set up dev bat0
$ sudo ip link set up dev bat-bridge
```

Mmmm... `wlan0` will not accept a master. I tried this with the device down as well.

Lets try to get an address on the brand new and promising `bat-bridge`.

```text
$ sudo dhcpcd bat-bridge
DUID 00:01:00:01:19:8d:d2:59:90:f6:52:17:92:06
bat-bridge: IAID d9:3b:62:ea
bat-bridge: soliciting an IPv6 router
bat-bridge: soliciting a DHCP lease
bat-bridge: no IPv6 Routers available
timed out
dhcpcd exited
```

This is unfortunate.

Possible problems:

1. Bridging 2 wireless NICs instead of one wireless and one wired.
1. `wlan0`'s reluctance to having a master.
1. The `iwconfig` `ap` thingy.
