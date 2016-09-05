Title: An Adhoc Net for Quick File Transfer
Date: 2016-09-04 19:49
Category: play
Tags: networking, mesh, linux

# Introduction

Needing to transfer a lot of data between two computers, I find the perfect excuse to mess with the network.
Unfortunately, my ethernet cable is broken so wireless it will be.

Transfering file through the router has a rate of 1MB/s. I'm disgusted by this. To improve it, I'll try an adhoc network between the machines.

This article will be very similar and is based on my previous B.A.T.M.A.N. articles.

# Components

1. Custom built PC with a Qualcomm Atheros AR9300 WiFi and a current Arch Linux.
1. Acer Aspire E15 (E5-521-84UV) laptop with a Broadcom BCM43142 WiFi card and a current Arch Linux.

A current Arch has the 4.7.2 kernel.

# Objectives

1. Setup a direct connexion.
1. Transfer files faster than through the router.

# Configuration of an Ad-Hoc Connection

Since the machines are so similar, the instructions work almost verbatim with the exception of the device name.

```text
$ sudo iw dev wlan0 set type ibss
$ sudo ip link set up dev wlan0
$ sudo iw dev wlan0 ibss join openadhoc 2472

$ iw dev wlan0 info
Interface wlan0
	ifindex 3
	wdev 0x1
	addr 90:f6:52:17:92:06
	ssid openadhoc
	type IBSS
	wiphy 0
	channel 5 (2432 MHz), width: 20 MHz (no HT), center1: 2432 MHz
```

This sets both devices to the same channel as peers. Surprisingly, to channel 1 when I asked for channel 13.

`ping` works immediatelly! :D

A `iw dev wlan0 station dump` shows that a connection is established:

```text
Station d0:53:49:c0:05:6a (on wlan0)
	inactive time:	66 ms
	rx bytes:	85589
	rx packets:	1048
	tx bytes:	0
	tx packets:	0
	tx retries:	0
	tx failed:	0
	rx drop misc:	0
	signal:  	-40 [-51, -40, -55] dBm
	signal avg:	-37 [-55, -37, -48] dBm
	tx bitrate:	1.0 MBit/s
	rx bitrate:	6.0 MBit/s
	authorized:	yes
	authenticated:	yes
	associated:	yes
	preamble:	long
	WMM/WME:	yes
	MFP:		no
	TDLS peer:	no
	DTIM period:	0
	beacon interval:100
	connected time:	228 seconds
```

Suprisingly, on the laptop (Broadcom), the `station dump` is empty.

The IP is provided by the IPv6 autoconfiguration and there's name resolution through Zeroconf.

There are two strange things. The first one is that the ping takes a second or two to begin.
The second is that the RTT is around a ms (rtt min/avg/max/mdev = 0.999/1.855/9.690/2.092 ms).

Unfortunately, SSH does not. I suppose it doesn't bind to link scoped addresses.

To autoconfigure an IP address, I used `sudo avahi-autoipd -D wlan0`.

# Transfering files

With `rsync`, I get ~1MB/s. A little dissapointed but I'm sure it can be improved.

Lets try Deluge: 1.5MB/s. A definite improvement but I'm not satisfied.

Lets mess with the NICs. Lets change retry to 2 and disable power save.

Now `rsync` does ~1.8MB/s. That's a nice improvement but still dissapointing.
Deluge, on the other hand, is doing 5MB/s. This is great!

I mean, it's pathetic but for WiFi 11n HT20 (Broadcom), it's pretty good.

I guess I'll disable power save on my laptop!
