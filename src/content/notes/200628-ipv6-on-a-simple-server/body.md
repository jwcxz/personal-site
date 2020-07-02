My hosting provider assigns a block of IPv6 addresses for each plan, so I
thought I would enable them on my plans.  Overall, the process is fairly
simple, but it took some studying on my part to understand what had to be done
and the "right way" of doing things.  This is a quick summary of what I did.


<!--break-->


## Network Stack Setup

I use
[systemd.network](https://www.freedesktop.org/software/systemd/man/systemd.network.html)
to configure each server's network.

To enable a [dual-stack](https://whatismyipaddress.com/dual-stack) IPv4/IPv6
configuration, I set up `/etc/systemd/network/10-wired.network` as follows:

```ini
[Match]
Name=<Interface Name>

[Network]
DHCP=No
DNS=8.8.8.8
Address=YYYY:YYYY:YYYY:YYYY:YYYY:YYYY:YYYY:YYYY/YYY
Gateway=GGG.GGG.GGG.1
Gateway=HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:1

[Address]
Label=static-ipv4
Address=XXX.XXX.XXX.XXX/32
Peer=GGG.GGG.GGG.1/32
```

I followed this pattern from a [guide I
found](https://wiki.hetzner.de/index.php/Network_configuration_using_systemd-networkd/en).
I think that it should be possible to do away with the `Peer` configuration and
adjust the address mask to approach things more traditionally, as this was
highlighted as a way to deal with being assigned an address entirely
independent of the gateway.


## Firewall Configuration

I decided to use opportunity to move to
[nftables](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page), and
patterned my implementation on [this example
ruleset](https://wiki.nftables.org/wiki-nftables/index.php/Simple_ruleset_for_a_server).
nftables' clear syntax and useful constructs like sets and dictionaries made
configuration a painless process.  I switched my boxes at home to use nftables
as well home to use nftables as well.


## Fail2ban Configuration

As a consequence of moving to nftables (not related to enabling IPv6 support),
I modified my Fail2ban configuration to ban via nftables as well.

This was simply a matter of adding `banaction = nftables` into the `[DEFAULT]`
section of `/etc/fail2ban/jail.local`.


## Service Configuration

Most services will natively listen on IPv6 addresses out of the box.  Postfix
and nginx required a few minor changes.


### Postfix

I made a few updates to `/etc/postfix/main.cf` by following the [IPv6 support
instructions](http://www.postfix.org/IPV6_README.html) on Postfix's site.


### nginx

I read a few thoughts on the best way to listen on both IPv4 and IPv6 stacks,
[this
one](https://serverfault.com/questions/638367/do-you-need-separate-ipv4-and-ipv6-listen-directives-in-nginx)
being the most informative.

I ultimately ended up replacing all of my existing `listen` directives with:

```plaintext
listen 80;
listen [::]:80;
listen 443 ssl;
listen [::]:443 ssl;
```


## DNS Configuration

Finally, I added the server's IP address as a new `AAAA` record and updated the SPF record to include the `ip6` field:

```plaintext
v=spf1 ip4:XXX.XXX.XXX.XXX ip6:YYYY:YYYY:YYYY:YYYY:YYYY:YYYY:YYYY:YYYY -all
```


## Verification

[This tool](https://ready.chair6.net) was a helpful way to quickly check that
things were functional, as I've not enabled IPv6 on my home network yet.
Unfortunately my host's nameservers do not have IPv6 addresses, so the results
are not fully compliant.

I also verified that all expected services were listening on both IPv4 and IPv6
addresses via `netstat -l`.
