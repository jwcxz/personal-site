These are some notes on setting up a small mail server suitable for a single
user or a few users.

This setup uses the following projects to enable sending and receiving mail
using SPF, DKIM, and DMARC for email authentication:

* [Postfix](http://www.postfix.org) for mail transfer and delivery to Dovecot
  via LMTP.

* [Dovecot](https://dovecot.org) for IMAP access and SASL for Postfix with
  [Pigeonhole](https://pigeonhole.dovecot.org) for Sieve message filtering
  support

* [Rspamd](https://rspamd.com) for spam filtering, email authentication
  validation, and DKIM signing (with [Redis](https://redis.io) for caching)

* [Let's Encrypt](https://letsencrypt.org) and
  [certbot](https://certbot.eff.org) to provide SSL certs

Moreover this configuration enables support for sending and receiving mail on
two domains whereby the two domains mirror each other.


<!--break-->


The configuration described below is cumulative --- it requires that all of the
projects are used.  I've tried to call out specific linkages where possible.
These notes are intended to be comprehensive in that they should describe all
of the pieces necessary to enable a functional mail server.


[[toc]]


## Certificates and Keys

### SSL/TLS Certs

Obtain an SSL certificate from Let's Encrypt.  This particular server did not
have an existing HTTP server, so I used certbot in standalone mode:

```plaintext
# certbot certonly --standalone -d domain1.tld,domain2.tld
```

This produces a single certificate for both domains.  Alternatively, one could
invoke certbot for each domain to produce separate certificates.


### DKIM Keys

Rspamd includes a utility to generate DKIM keys.  I created a directory within
`/etc/rspamd`, protected it, and generated keys according to Rspamd's
[`dkim_signing` guide](https://rspamd.com/doc/modules/dkim_signing.html).

```plaintext
# mkdir -p /etc/rspamd/dkim/keys
# chown -R rspamd:rspamd /etc/rspamd/dkim
# chmod -R 700 /etc/rspamd/dkim
# rspamadm dkim_keygen -s 'mail' -b 2048 -d domain1.tld -k /etc/rspamd/dkim/keys/domain1.tld.mail.key > /etc/rspamd/dkim/keys/domain1.tld.mail.txt
# rspamadm dkim_keygen -s 'mail' -b 2048 -d domain1.tld -k /etc/rspamd/dkim/keys/domain2.tld.mail.key > /etc/rspamd/dkim/keys/domain2.tld.mail.txt
# chown rspamd:rspamd /etc/rspamd/dkim/keys/*
# chmod 600 /etc/rspamd/dkim/keys/*
```

If you are having trouble splitting up the public key into
[multiple chunks within the DNS TXT record](http://hack.limbicmedia.ca/how-to-split-dns-dkim-records-properly/),
you may need to use `-b 1024` and live with the weakened security.


### Diffie-Hellman Parameters for Dovecot

This is actually optional because I disabled non-ECC Diffie-Hellman ciphers
in the Dovecot configuration.

```plaintext
# touch /etc/dovecot/dh.pem
# chmod 600 /etc/dovecot/dh.pem
# chown root:root /etc/dovecot/dh.pem
# openssl dhparam -out /etc/dovecot/dh.pem 4096
```



## Postfix Configuration

The following Postfix configuration enables SASL through Dovecot, delivers mail
to Dovecot's LMTP service, enables TLS, and enables Rspamd as a milter.

I've only listed variables that differ from the defaults as of Postfix 3.9.

```plaintext
# based on Postfix 3.9.0
compatibility_level = 3.9

# Restrictions
# smtpd_recipient_restrictions includes the following features:
#   1.  prohibit specific senders via check_sender_access
#       create a list of prohibited domains in the following format
#           baddomain.tld   REJECT
#       save to /etc/postfix/sender_access and run `postmap /etc/postfix/sender_access`
#   2.  prepend X-Original-To for LMTP via check_recipient_access and set
#       lmtp_destination_recipient_limit
#       see https://dovecot.dovecot.narkive.com/jYiqyZYr/differences-in-delivered-to-header-between-deliver-and-lmtp#post7
smtpd_recipient_restrictions =  check_sender_access lmdb:/etc/postfix/sender_access,
                                check_recipient_access pcre:{{/(.+)/ prepend X-Original-To: $$1}}
lmtp_destination_recipient_limit = 1

# SMTP smuggling protection
# See https://www.postfix.org/smtp-smuggling.html
# `yes` is the default for Postfix 3.9+
smtpd_forbid_bare_newline = yes

# Recognized local recipients
# The default value includes both unix:passwd.byname and $alias_maps.  The
# former causes Postfix to initially recognize any system user account, but
# when trying to deliver mail to an account that won't accept it (e.g. system
# accounts), Dovecot will return a failure, causing Postfix to bounce the
# incoming email instead of rejecting it.  This, in turn, creates a backscatter
# pathway for spammers (e.g. if a system has a `git` system account that
# doesn't receive mail, a spammer can send an email with a spoofed From address
# to git@domain.tld and Postfix would send a bounce email to the spoofed From
# address).  The solution is to only recognize the aliases in /etc/aliases.
# Make sure to put a self-reference in /etc/aliases (`<user>: <user>`).
local_recipient_maps = $alias_maps

# Aliases
alias_maps = lmdb:/etc/postfix/aliases
alias_database = $alias_maps

# Network
# set because $myhostname is domain.tld (not server.domain.tld)
mydomain = $myhostname
# set in order to add secondary domain
#   alternative is to use virtual domains: http://www.postfix.org/VIRTUAL_README.html
mydestination = $myhostname, localhost.$mydomain, localhost, localhost.localdomain, domain2.tld

# TLS support
smtpd_use_tls = yes
smtpd_tls_loglevel = 1
smtpd_tls_cert_file = /etc/letsencrypt/live/domain1.tld/fullchain.pem
smtpd_tls_key_file  = /etc/letsencrypt/live/domain1.tld/privkey.pem
smtpd_tls_session_cache_database = lmdb:/var/lib/postfix/smtpd_scache
smtp_tls_session_cache_database  = lmdb:/var/lib/postfix/smtp_scache

# SASL support
smtpd_sasl_auth_enable = yes
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth

# Milters
#smtpd_milters = unix:/var/lib/rspamd/milter.sock
# or for TCP socket
smtpd_milters = inet:localhost:11332
non_smtpd_milters = $smtpd_milters
#milter_mail_macros = i {mail_addr} {client_addr} {client_name} {auth_authen}
# skip mail without checks if something goes wrong
milter_default_action = accept

# Delivery
mailbox_transport = lmtp:unix:private/dovecot-lmtp

# Others
recipient_delimiter = +
biff = no
```

To enable "Submission" (port 587) for client usage, the following can be added
to `/etc/postfix/master.cf`:

```plaintext
submission inet n       -       n       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_tls_auth_only=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
```

*Edit 2021-09-29*: `smtpd_tls_cert_file` now points at the full chain instead
of the individual cert.

*Edit 2022-02-13*: `smtpd_recipient_restrictions` uses Postfix 3.7's inline
`pcre:{{}}` syntax rather than requiring a separate file.

*Edit 2024-01-12*: Added `smtpd_forbid_bare_newline` to protect against [SMTP
smuggling](https://www.postfix.org/smtp-smuggling.html) attacks on Postfix
3.8.4 (it's enabled by default on 3.9+).

*Edit 2024-08-15*: Changed `hash:` and `btree:` to `lmdb:`.

*Edit 2024-08-23*: Changed `local_recipient_maps` from its default value to
just `$alias_maps` to prevent backscatter using system accounts.


### Supporting Multiple Domains

In this configuration, I opted to serve multiple domains in the simplest way,
by adding the second domain to `mydestination`.  Postfix's
[guide](http://www.postfix.org/VIRTUAL_README.html) on this subject describes
this way as being useful for the situation where each user receives mail in
each domain, which was the case that applied to me.  For more complex usages,
one could use virtual alias domains, also described in that guide.


### Relay vs. Recipient Restrictions

Postfix has a [document that describes access
restrictions](http://www.postfix.org/SMTPD_ACCESS_README.html).  It notes that
as of Postfix 2.10, the `smtpd_relay_restrictions` takes care of preventing
Postfix from acting as an open relay.  As such, many Postfix configuration
tutorials do not have up-to-date guidance; instead, they opt to carefully
configure `smtpd_recipient_restrictions`.  As Postfix's document illustrates,
either way will work, so long as one of them prevents Postfix from acting as an
open relay.  In this configuration, I am relying on the sane default
configuration of `smtpd_relay_restrictions`, which `postconf -d
smtpd_relay_restrictions` reports to be:

```plaintext
smtpd_relay_restrictions = ${{$compatibility_level} < {1} ? {} : {permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination}}
```

Optionally, you can use `smtpd_recipient_restrictions` to prohibit certain
domains.  In my case, an attacker has been trying to sign up for an unprotected
service by using fake emails from my domain name.  I reject all emails from
that service.

*Edit 2020-07-06*: Per
[this discussion](https://dovecot.dovecot.narkive.com/jYiqyZYr/differences-in-delivered-to-header-between-deliver-and-lmtp#post7),
I have added a `check_recipient_access` entry that adds an `X-Original-To`
header containing the original address that the email was intended for.  Paired
with the adjustment of the Dovecot configuration variable
`lda_original_recipient_header`, this makes Sieve filtering based on address
and "detail" (label after the `+` in an address) fairly simple.



## Dovecot

I structured `/etc/dovecot` to follow the example template provided with
Dovecot.

```plaintext
# mkdir -p /etc/dovecot
# cp -R /usr/share/doc/dovecot/example-config/conf.d /etc/dovecot
# cp -R /usr/share/doc/dovecot/example-config/dovecot.conf /etc/dovecot
```

Importantly, I had to make a few changes to the files in `conf.d/`:

1.  Because I am using passwd-file authentication, I commented out the
    inclusion of `auth-system.conf.ext` in `conf.d/10-auth.conf`:

    ```plaintext
    #!include auth-system.conf.ext
    ```

2.  Because SSL certs are located in `/etc/letsencrypt`, I commented out the
    attempts to read in those certs in `conf.d/10-ssl.conf`:

    ```plaintext
    #ssl_cert = </etc/ssl/certs/dovecot.pem
    #ssl_key = </etc/ssl/private/dovecot.pem
    ```

    I suppose one could symlink the certs to these locations instead.

I then made changes from the default configuration (as of Dovecot 2.3.10.1) by
creating the following `/etc/dovecot/local.conf`.  Dovecot will [merge this
configuration](https://doc.dovecot.org/configuration_manual/config_file/config_file_syntax/)
with the existing defaults.

```plaintext
protocols = imap lmtp

# conf.d/10-auth.conf

auth_mechanisms = plain login
!include conf.d/auth-passwdfile.conf.ext


# conf.d/10-mail.conf

mail_location = maildir:~/.mail


# conf.d/10-master.conf

service lmtp {
    unix_listener /var/spool/postfix/private/dovecot-lmtp {
        mode  = 0600
        user  = postfix
        group = postfix
    }
}

service auth {
    unix_listener /var/spool/postfix/private/auth {
        mode  = 0666
        user  = postfix
        group = postfix
    }
}


# conf.d/10-ssl.conf

ssl_cert = </etc/letsencrypt/live/domain1.tld/fullchain.pem
ssl_key  = </etc/letsencrypt/live/domain1.tld/privkey.pem
ssl_min_protocol = TLSv1.2
ssl_cipher_list = ALL:!DH:!kRSA:!SRP:!kDHd:!DSS:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK:!RC4:!ADH:!LOW@STRENGTH
ssl_prefer_server_ciphers = yes


# conf.d/15-lda.conf

lda_original_recipient_header = X-Original-To


# conf.d/20-imap.conf

protocol imap {
    mail_max_userip_connections = 20
}


# conf.d/20-lmtp.conf

protocol lmtp {
    mail_plugins = $mail_plugins sieve
}
```

As a consequence, Dovecot provides a
[SASL service](https://wiki2.dovecot.org/HowTo/PostfixAndDovecotSASL)
to Postfix for authentication and receives mail from Postfix
[via LMTP](https://wiki.dovecot.org/HowTo/PostfixDovecotLMTP).  It enables an
IMAP service for mail user agent connection.

*Edit 2020-07-06*: The adjustment to `lda_original_recipient_header` (which
also applies to LMTP) tells Dovecot to use the `X-Original-To` header to
specify the original recipient.

Following
[Mozilla's TLS guide](https://wiki.mozilla.org/Security/Server_Side_TLS), the
minimum protocol is set to `TLSv1.2`.  A more restrictive set of ciphers are
allowed as well (in particular, no non-ECC Diffie-Hellman support).


*Edit 2021-09-29*: `ssl_cert` now points at the full chain instead of the
individual cert.


### User Authentication

This configuration uses a simple password file for authentication.

```
touch /etc/dovecot/users
chown dovecot:dovecot /etc/dovecot/users
chmod 600 /etc/dovecot/users
```

Passwords can be generated with `dovecot pw -s SHA512-CRYPT` as per [Dovecot's
password scheme guide](https://doc.dovecot.org/configuration_manual/authentication/password_schemes/#authentication-password-schemes).

Then, following
[Dovecot's Passwd-file guide](https://doc.dovecot.org/configuration_manual/authentication/passwd_file/),
one can create a mostly-empty row in `/etc/dovecot/users`:

```plaintext
user:{SHA512-CRYPT}<hash>:sys_user:sys_user_group::/home/sys_user::
```

This configuration allows for a virtual mapping from `user` to the system
account `sys_user` with its corresponding group `sys_user_group` and home
directory `/home/sys_user`.  `user` should be the account that you map all of
your aliases in `/etc/postfix/aliases` to.



## Redis Configuration

*Edit 2022-01-29*: The Rspamd-Redis connection now uses UNIX sockets.

Per [Rspamd's Quick Start guide](https://rspamd.com/doc/quickstart.html), I
adjusted a few Redis configuration settings slightly, namely setting a memory
limit and policy and enabling access via UNIX socket.  To do that, I added
`include /etc/redis.d/local.conf` to the end of `/etc/redis.conf` and created
the following `/etc/redis.d/local.conf`:

```plaintext
# settings recommended by Rspamd
#   https://rspamd.com/doc/quickstart.html

maxmemory 500mb
maxmemory-policy volatile-ttl
unixsocket /var/run/redis/redis.sock
unixsocketperm 770
```

I also followed the suggestion of setting `vm.overcommit_memory = 1` with
sysctl and in `/etc/sysctl.d/`.



## Rspamd

[Rspamd](https://rspamd.com) is a powerful spam filtering tool that can also be
used to add DKIM signatures to outgoing messages.  I have used it since ~v1.2
(mid-2016); it has grown significantly since then, and there have been a few
configuration-breaking changes in that time.  However, I have not encountered
such issues recently.

Rspamd has an elegant and flexible configuration syntax which is described in
[this document](https://rspamd.com/doc/configuration/index.html).

I generally followed the
[Quick Start guide](https://rspamd.com/doc/quickstart.html) as well as the
[DKIM signing documentation](https://rspamd.com/doc/modules/dkim_signing.html)
to set up Rspamd to act as a Postfix milter, block spam with mostly-default
settings, and utilize greylisting.

I made changes exclusively within `/etc/rspamd/local.d` and only included
settings that changed the defaults as of Rspamd 2.5.


### Global Configuration Settings

I have [Unbound](https://nlnetlabs.nl/projects/unbound/about/) configured as
the local nameserver, so Rspamd will automatically use it (`/etc/resolv.conf`
points to `127.0.0.1`).  Rspamd can generate a lot of DNS requests, so I have
found this to be a valuable solution.  Using a public nameserver will likely
result in rejections over time.

Therefore, `local.d/options.inc` looks like:

```plaintext
# same as postfix $mynetworks minus loopback addresses (`postconf mynetworks`)
local_addrs = [
    <self IP addresses>
];

# DNS tuning for local DNS server
#   probably not necessary
dns {
    timeout = 10s;
    retransmits = 50;
}

# server does not support SSE3
disable_hyperscan = true;
```


### Proxy Worker as Milter

The Rspamd proxy worker acts as a milter by default, but should be configured
to scan outbound mail to DKIM sign messages.  That can be accomplished by
setting the following in `local.d/worker-proxy.inc`:

```plaintext
upstream "local" {
    self_scan = yes;
}

# spawn more processes in self-scan mode
count = 4;
```


### DKIM Signing

Because each DKIM key follows a structured file naming format,
`local.d/dkim_signing.conf` is relatively simple:

```plaintext
# the same settings apply for all domains

selector = "mail";
path = "/etc/rspamd/dkim/keys/$domain.$selector.key";
allow_username_mismatch = true;
```


### Spam Blocking Configuration

For testing, it's best to avoid outright rejecting emails that have a high spam
score.  The following adjustment in `local.d/actions.conf` adds spam headers
to pretty much all messages that exceed the (default) `add_header` threshold.

```plaintext
# always add headers instead of rejecting
reject = 500;
```

The following files enable and configure their respective modules to use Redis
as a backend.

*Edit 2022-01-29*: The Rspamd-Redis connection now uses UNIX sockets.

Rspamd connects to Redis via a UNIX socket (per
[these instructions](https://github.com/rspamd/rspamd/issues/1905)).  To
provide Rspamd access, its user must be added to the `redis` group via `usermod
-a -G redis rspamd` (note that some installations may have different
usernames for Rspamd).

`local.d/classifier-bayes.conf`:

```plaintext
backend = "redis";
```

`local.d/mx_check.conf`:

```plaintext
enabled = true;
```

`local.d/redis.conf`:

```plaintext
servers = "/var/run/redis/redis.sock";
```


### Sieve Configuration

Adding the following to `~/.dovecot.sieve` will send mail marked as spam to the Junk folder:

```plaintext
require ["fileinto"];

if header :is "X-Spam" "Yes" {
    fileinto "Junk";
    stop;
}
```



## Firewall

The firewall should open SMTP ports 25 and 587 and IMAP ports 143 and 993 to
appropriate network traffic.  For nftables, the following configuration can be
added to an input inet filter chain:

```plaintext
tcp dport { 25, 587 }  accept comment "Allow SMTP/Submission"
tcp dport { 143, 993 } accept comment "Allow IMAP/IMAPS"
```



## DNS

DNS entries need to be added for reverse DNS, SPF, DKIM, and DMARC.  These
tools all help other mail servers realize that your mail is not spam.  Of
course, an MX record is required as well.


### Reverse DNS PTR record

For the domain name that matches `$myhostname` in Postfix (not any other
domains), a PTR record is necessary.  For example, for an IP address of
1.2.3.4:

```plaintext
4.3.2.1.in-addr.arpa. 3599 IN    PTR     domain1.tld.
```

An equivalent IPv6 PTR record is necessary, too.
[This tool](http://rdns6.com/hostRecord) is helpful in generating the record.


### SPF Record

For all domains, an SPF record is required:

```plaintext
domain1.tld.    3599    IN      TXT     "v=spf1 ip4:<IPv4 Address> ip6:<IPv6 Address> -all"
```


### DKIM Record

Each of the DKIM keys generated [above](#dkim-signing) also generated a DNS
record in `/etc/rspamd/dkim/keys/$domain.$selector.txt`.  Each domain's record
must be added.


### DMARC Record

Adding a DMARC record to each domain helps other mail servers understand what
to do with mail that failed SPF or DKIM checks.  For testing, it makes sense to
ask the mail server to keep the mail but send reports back to you.

```plaintext
_dmarc.domain1.tld. 3599    IN      TXT     "v=DMARC1; p=none; pct=100; rua=mailto:dmarc-reports@domain1.tld"
```

By changing to `p=reject`, the other server will reject mail that failed these
checks.

[This guide](https://postmarkapp.com/guides/dmarc) provides a helpful overview
of DMARC.



## User Mail Directory

I opted to place mail in `~/.mail`, so I created the appropriate inbox directory:

```plaintext
$ mkdir -p ~/.mail/{cur,new,tmp}
$ mkdir -p ~/.mail/.{Sent,Drafts,Trash,Junk}/{cur,new,tmp}
```



## Conclusion

After enabling and starting Redis, Rspamd, Dovecot, and Postfix, (and reloading
the firewall configuration), everything should (hopefully) be functional.
After confirming that your server is safely sending and receiving emails, you
might consider changing the DMARC policy and rejecting mail with high spam
scores.

I found these tools to be helpful in debugging:

* https://www.mail-tester.com
* https://ismyemailworking.com
* https://www.dmarcanalyzer.com

The [Mail Server](https://wiki.archlinux.org/index.php/Mail_server) page on the
Arch Wiki lists a few others.



## Extra Credit: Fail2ban

[Fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) works nearly out
of the box.  A small configuration like this one (as
`/etc/fail2ban/jail.local`) will ban offenders to Postfix and Dovecot for 90
days and send an email upon performing the ban.


```plaintext
[DEFAULT]
destemail = user@domain1.tld
sender = user@domain1.tld

action = %(action_mw)s

banaction = nftables

bantime = 90d


[postfix-sasl]
enabled = true

[dovecot]
enabled = true
```
