Title: B.A.T.M.A.N
Date: 2016-02-28 21:48
Category: play
Tags: networking, mesh, linux

# Introduction

After much dissapointment with 802.11s, I'm ready to try the other alternatives.

I've learned that small steps are benefitial in these faulty lands so I'll setup an ad-hoc connection first and after I see that it works, I'll setup BATMAN.

BATMAN has gone through some deep changes during it's life. AFAIK, it begun as a layer 3 thingy and later became a layer 2 thingaru. With zero network experience, I'm of the opinion that layer 2 is the correct layer for a service of this kind.

A bit of weirdness introduced by being layer 2 is that all the nodes will appear to be directly connected to each other. I find this unfortunate as the tools I normally use become deceptive. `batctl` provides alternatives which understand what's actually going on.

# Components

1. Custom built PC with a Qualcomm Atheros AR9300 WiFi and a current Arch Linux.
1. Acer Aspire E15 (E5-521-84UV) laptop with a Broadcom BCM43142 WiFi card and a current Arch Linux.

A current Arch has the 4.4.1 kernel.

IBSS does not appear to be usable with other configurations on the Atheros WiFi:

```text
$ iw list
[...]
	valid interface combinations:
		 * #{ managed } <= 2048, #{ AP, mesh point } <= 8, #{ P2P-client, P2P-GO } <= 1,
		   total <= 2048, #channels <= 1, STA/AP BI must match
		 * #{ WDS } <= 2048,
		   total <= 2048, #channels <= 1, STA/AP BI must match
[...]
```

Broadcom supports no combinations, of course.

# Objectives

1. Setup an ad-hoc connection.
1. Setup a mesh connection between the two machines with static IPs. To test the connection, `ping` would be an good first test.

# Configuration of an Ad-Hoc Connection

Since the machines are so similar, the instructions work almost verbatim with the exception of the device name.

```text
$ sudo iw dev wlan0 set type ibss
$ sudo ip addr add 192.168.2.5/24 dev wlan0
$ sudo ip link set up dev wlan0
$ sudo iw dev wlan0 ibss join openadhoc 2432

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

This sets both devices to the same channel as peers.

`ping` works immediatelly! :D

A `iw dev wlan0 station dump` shows that a connection is established:

```text
$ iw dev wlan0 station dump
Station d0:53:49:c0:05:6a (on wlan0)
	inactive time:	356 ms
	rx bytes:	17746
	rx packets:	223
	tx bytes:	832
	tx packets:	8
	tx retries:	0
	tx failed:	0
	signal:  	-41 [-45, -45, -49] dBm
	signal avg:	-41 [-45, -45, -51] dBm
	tx bitrate:	48.0 MBit/s
	rx bitrate:	54.0 MBit/s
	expected throughput:	3.414Mbps
	authorized:	yes
	authenticated:	yes
	preamble:	long
	WMM/WME:	yes
	MFP:		no
	TDLS peer:	no
```

Suprisingly, on the laptop (Broadcom), the `station dump` is empty.

# Configuration of BATMAN

To guide me, I'm reading the [quick-start from Open-Mesh.org](https://www.open-mesh.org/projects/batman-adv/wiki/Quick-start-guide).

I need some new stuff on my system for this to work: `yaourt -S batctl`

OK, LET'S DO THIS!!

The quick-start uses an ethernet link for the example, which is not very helpful, and does not mention something crucial for WiFi.

BATMAN will work over any link. That means that it would work over ethernet, ad-hoc or managed. You have to configure the device to the type you want. BATMAN will not change that.

First configure the device:

```text
$ sudo iw dev wlan0 set type ibss
$ sudo ip link set up dev wlan0
$ sudo iw dev wlan0 ibss join openbatman 2432
```

Now configure BATMAN:

```text
$ sudo modprobe batman-adv
$ sudo batctl if add wlan0
$ sudo ip link set up dev wlan0
$ sudo batctl if
wlan0: active
$ sudo journalctl -f
[...]
Feb 28 22:22:35 epictetus kernel: batman_adv: bat0: Adding interface: wlan0
Feb 28 22:22:35 epictetus kernel: batman_adv: bat0: The MTU of interface wlan0 is too small (1500) to handle the transport of batman-adv packets. Packets going over this interface will be fragmented on layer2 which could impact the perform
Feb 28 22:22:35 epictetus kernel: batman_adv: bat0: Not using interface wlan0 (retrying later): interface not active
[...]
Feb 28 22:24:43 epictetus kernel: IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
Feb 28 22:24:43 epictetus kernel: batman_adv: bat0: Interface activated: wlan0
[...]
$ sudo ip addr add 192.168.2.5/24 dev bat0
$ sudo ip link set up dev bat0
```

And it works! :D
