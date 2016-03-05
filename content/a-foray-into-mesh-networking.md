Title: A Foray into Mesh Networking
Date: 2016-02-28 19:26
Category: play
Tags: networking, mesh, linux

# Introduction

When I learned about mesh networks, I immediately found it appealing and begun craving for one. That was over ten years ago.

I honestly didn't understand why consumer level network configuration tools (like NetworkManager) don't have the option to join or setup a mesh.

On this article I'll document my impressions into a light attempt to get the most basic mesh functionality using 802.11s.

# Components

1. Custom built PC with a Qualcomm Atheros AR9300 WiFi and a current Arch Linux.
1. Acer Aspire E15 (E5-521-84UV) laptop with a Broadcom BCM43142 WiFi card and a current Arch Linux. There are several drivers for Broadcom cards but I can only use the `wl` driver which does not support mesh mode. :(
1. D-Link DWA-110 USB WiFi to make up for the sucky Broadcom driver.

A current Arch has the 4.4.1 kernel.

I did not include my router as it has a super old OpenWRT 12.09 from 2012.

# Objective

Setup a mesh connection between the two machines with static IPs. To test the connection, `ping` would be an good first test.

# Configuration

Since the machines are so similar, the instructions work almost verbatim with the exception of the device name.

```text
sudo iw dev wlan0 set type mesh
sudo ip addr add 192.168.2.5/24 dev wlan0
sudo ip link set up dev wlan0
sudo iw dev wlan0 mesh join openmesh

iw dev wlan0 info
Interface wlan0
	ifindex 3
	wdev 0x1
	addr 90:f6:52:17:92:06
	type mesh point
	wiphy 0
	channel 1 (2412 MHz), width: 20 MHz (no HT), center1: 2412 MHz
```

This sets both devices to the same channel as mesh points.

A `iw dev wlan0 station dump` shows that a connection is established:

```text
iw dev wlan0 station dump
Station 00:1b:11:20:dc:2c (on wlan0)
	inactive time:	486 ms
	rx bytes:	7577
	rx packets:	116
	tx bytes:	174
	tx packets:	3
	tx retries:	7
	tx failed:	0
	signal:  	-25 [-28, -30, -33] dBm
	signal avg:	-26 [-29, -31, -33] dBm
	Toffset:	-262757995 us
	tx bitrate:	48.0 MBit/s
	rx bitrate:	9.0 MBit/s
	mesh llid:	22429
	mesh plid:	44255
	mesh plink:	ESTAB
	mesh local PS mode:	ACTIVE
	mesh peer PS mode:	ACTIVE
	mesh non-peer PS mode:	ACTIVE
	authorized:	yes
	authenticated:	yes
	preamble:	long
	WMM/WME:	yes
	MFP:		no
	TDLS peer:	no
```

The `arping` tool gets a reply:

```text
sudo arping -I wlan0 192.168.2.3
ARPING 192.168.2.3 from 192.168.2.5 wlan0
Unicast reply from 192.168.2.3 [00:1B:11:20:DC:2C]  8.153ms
^CSent 32 probes (1 broadcast(s))
Received 1 response(s)
```

The ARP table gets a new entry:

```text
arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.2.3              ether   00:1b:11:20:dc:2c   C                     wlan0
```

The mesh path, looks good.

```text
sudo iw dev wlan0 mpath dump
DEST ADDR         NEXT HOP          IFACE	SN	METRIC	QLEN	EXPTIME		DTIM	DRET	FLAGS
00:1b:11:20:dc:2c 00:1b:11:20:dc:2c wlan0	17	342	0	0	100	0	0x4
```

Unfortunately, `ping` does not work.

```text
ping 192.168.2.3
PING 192.168.2.3 (192.168.2.3) 56(84) bytes of data.
^C
--- 192.168.2.3 ping statistics ---
20 packets transmitted, 0 received, 100% packet loss, time 19008ms
```

After trying many things, I could not get this to work.

I suspect either I'm doing something wrong or there's a problem with a driver or equipment.

Given that my equipment (the USB dongle and the disappointing Broadcom WiFi) is pretty lousy, I'll try again when I get better hardware.
