For the purposes of experimentation, I set up a simple WireGuard configuration
that designates one peer as a "server" and the others as "clients" to provide a
VPN.  Clients can connect to the internet while masked behind the server (as
one would expect from a VPN) and can also interact with certain other clients.
The server also acts as a DNS server to the clients.

A few notes follow on how I set this configuration up using
[WireGuard](https://www.wireguard.com), [nftables](http://nftables.org), and
[Unbound](https://nlnetlabs.nl/projects/unbound/about/), as well as a script
for automating the process of adding new clients.


<!--break-->


[[toc]]


## WireGuard Setup

The Arch Linux Wiki has an [excellent
guide](https://wiki.archlinux.org/index.php/WireGuard) for configuring
WireGuard.  I opted to use `wg-quick` for persistent configuration management.

Note that this configuration is IPv4-only, but can be extended to support IPv6.

This example assumes that clients live within the address space `10.0.0.2`
through `10.0.0.254`.


### Server Configuration

The WireGuard server configuration (e.g. `/etc/wireguard/wg0.conf`) looks like
this:

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <Server Private Key>

[Peer]
PublicKey = <Client A Public Key>
PresharedKey = <Client A Pre-Shared key>
AllowedIPs = 10.0.0.20/32

[Peer]
...
```

Because my setup uses nftables, I opted to statically configure it rather than
supply `PreUp`/`PostUp`/`PreDown`/`PostDown` hooks in the server configuration.


### Client Configuration

To create a new client, the following steps must be performed:

1. Generate a private key (`wg genkey`) and pre-shared key (`wg genpsk`) for
   that client.

2. Create a client configuration file (which should be securely sent to that
   client, e.g. with [qrencode](https://github.com/fukuchi/libqrencode)).

3. Add the client's pre-shared key and public key (`wg genpub`) to the server
   configuration.


For a full-tunnel configuration (all traffic is routed through the VPN), the
client configuration should look something like this:

```ini
[Interface]
Address = 10.0.0.20/24
PrivateKey = <Client Private Key>
DNS = 10.0.0.1

[Peer]
# server
Endpoint = <VPN Server Address>:51820
PublicKey = <Client Public Key>
PresharedKey = <Client Pre-Shared Key>
AllowedIPs = 0.0.0.0/0
```

For a split-tunnel configuration (only traffic destined for other clients in
the VPN network is routed through the VPN), `AllowedIPs` can instead be set to
`10.0.0.0/24`.

[Here is a simple script](add-wireguard-client.sh) that creates both split- and
full-tunnel configurations for a new client and adds that client as a peer to
the server configuration.  It should be run as `root`, since that is the only
user who should be allowed to access the `/etc/wireguard` directory.



## nftables Configuration

Configuring nftables is a matter of:

1. Opening the port that WireGuard listens on

2. Allowing WireGuard clients to make DNS requests

3. Forwarding client traffic to the internet

4. Masquerading that traffic so that it looks like it comes from the server

5. Allowing clients to access a restricted set of other clients


I followed [this
guide](https://xdeb.org/post/2019/09/26/setting-up-a-server-firewall-with-nftables-that-support-wireguard-vpn/)
to configure nftables.


The following definitions are relevant for the changes to `/etc/nftables.conf`:

```plaintext
define WAN_IFC      = ens0

define VPN_IFC      = wg0
define VPN_NET      = 10.0.0.0/24
define VPN_SERVICES = { 10.0.0.20, 10.0.0.21 }
```


### Opening WireGuard's listening port and allowing DNS requests

The following lines open WireGuard's port (51820 UDP) to anyone and DNS to only
the VPN interface from an IP address within the VPN network.  It's probably
possible to limit the latter by only one of those two qualifiers.

```plaintext
table inet filter {
    ...
    chain input {
        type filter hook input priority 0; policy drop;
        ...

        udp dport 51820                                 accept comment "Allow VPN"
        iifname $VPN_IFC udp dport 53 ip saddr $VPN_NET accept comment "Allow DNS for VPN"
    }
}
```


### Forwarding client traffic to the internet and hiding it

The addition below to the `forward` chain forwards traffic from clients to the
internet.  The addition to the `postrouting` chain makes the traffic look as
though it's coming from the server.

```plaintext
table inet filter {
    ...
    chain forward {
        type filter hook forward priority 0; policy drop;
        ...

        # forward WireGuard traffic, allowing it to access internet via WAN
        iifname $VPN_IFC oifname $WAN_IFC ct state new accept
    }
}

table ip router {
    # both prerouting and postrouting must be specified

    chain prerouting {
        type nat hook prerouting priority 0;
    }

    chain postrouting {
        type nat hook postrouting priority 100;

        # masquerade wireguard traffic
        # make wireguard traffic look like it comes from the server itself
        oifname $WAN_IFC ip saddr $VPN_NET masquerade
    }
}
```


### Allowing clients to access some other clients

If some clients provide services that other clients might want to use (e.g.
mail server, web server, etc.), nftables needs one more line of configuration
to forward traffic appropriately.  Accessible clients are defined by the
`VPN_SERVICES` set

```plaintext
table inet filter {
    ...
    chain forward {
        type filter hook forward priority 0; policy drop;
        ...

        # allow all clients to access those in the $VPN_SERVICES whitelist
        iifname $VPN_IFC oifname $VPN_IFC ip daddr $VPN_SERVICES ct state new accept
    }
}
```


## Packet Forwarding

The server must enable packet forwarding.  One can do this by creating a file
in `/etc/sysctl.d/` with the contents:

```plaintext
net.ipv4.ip_forward = 1
```

Analogous settings for IPv6 implementations also exist.


## DNS Configuration

Unbound works nearly out of the box.  At a minimum, the VPN IP address should
be added to the interfaces to listen on and access should be allowed to
clients:

```plaintext
server:
    ...
    interface: 10.0.0.1
    access-control: 10.0.0.0/24 allow
```

As usual, the [Arch Wiki](https://wiki.archlinux.org/index.php/unbound) has a
great guide on setting it up for more complex usages.  In particular, the
`private-domain` configuration feature can be used to set up an intranet of
sorts.
