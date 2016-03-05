Title: What Happened to Mesh Networking?
Date: 2015-10-11 21:20
Category: play
Tags: networking, mesh, linux

# Introduction

When I learned about mesh networks, I immediately found it appealing and begun craving for one. That was over ten years ago.

I honestly don't understand why consumer level network configuration tools (like NetworkManager) don't have the option to join or setup a mesh.

# Requirements

1. An AP is still required for machines not under my control.
1. Some sort of layer 2 or 3 encryption.

Optional:

1. Some nodes should be able to provide an AP into the mesh and configure non-mesh clients to be able to use Internet.
1. It should be smart and route at layer 3, not bridge the mesh nodes.
1. It should allow other people to use the mesh at lower priority for bandwidth.

# Hardware

1. Router: TP-Link TL-WR2543N/ND v1 (Atheros)
1. PC: Qualcomm Atheros AR93xx Wireless Network Adapter (rev 01)
1. Laptop: Broadcom
1. Etc: Windows, Mac, Android, iPhone.


The router uses OpenWRT 12.09 but I'll upgrade it to Chaos Calmer.

The PC and Laptop run Arch Linux.

The rest shall continue using the AP.

# Approach for Requirements

There are many ways to achieve this. Nothing as simple as I'd like.

## Standard 802.11s, AuthSAE & AHCP

Router: Everything should be supported by OpenWRT Chaos Calmer: http://wiki.openwrt.org/doc/howto/mesh.80211s

PC:

- 802.11s should be supported by the kernel directly.
- There's the ahcpd package in AUR and it builds.
- netctl doesn't support mesh as a connection type. Maybe a basic connection type plus scripts?
- The AuthSAE package from AUR doesn't build for me. Maybe create a separate PKGBUILD?

Laptop:

- (similar to PC)
- netctl-auto doesn't support mesh as a connection type. Maybe a basic connection type plus scripts?

## Standard Open 802.11s and VPN

Router:

- An open mesh can surely be configured.
- It has tinc for VPN.
- Can the open mesh not have access to Internet?
- Can BW for open mesh but not in VPN be given lower priority?

PC:

- 802.11s should be supported by the kernel directly.
- netctl doesn't support mesh as a connection type. Maybe a basic connection type plus scripts?
- Tinc has a package.
- How to only publish services on VPN?
- Can BW for open mesh but not in VPN be given lower priority?

Laptop:

- (similar to PC)
- netctl-auto doesn't support mesh as a connection type. Maybe a basic connection type plus scripts?


