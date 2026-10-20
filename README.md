# Netcat for Mere Mortals

**Netcat** — `nc` — is the command line's
bare hand on the network: one small tool
that opens a connection (or waits for one)
and then simply moves bytes between the
socket and your terminal or files. It
speaks no protocol. It has no opinions
about what the bytes mean. Whatever a
service says, you see; whatever you type,
the service gets. That emptiness is the
point: netcat is how you talk to a network
service *yourself*, by hand, when you want
to know what it actually says — and how
you stand up a listening ear in one line
when nothing else is installed.

It is the manual cousin of
[*Nmap for Mere Mortals*](https://paulsullivan33-dev.github.io/nmap-for-mere-mortals/):
nmap knocks on a thousand doors and
reports; netcat opens *one* door and has
the conversation. The rule of this guide
matches that guide's rule, stated in
chapter 1 and repeated until it's reflex:
**only connect to, and listen on, machines
you own or administer.** Everything here
is practised on a lab that lives entirely
on 127.0.0.1 — a banner-and-echo fixture
in `examples/lab_server.py`, a specimen
web page served by Python's built-in
server, and netcat listening to itself —
so the rule costs nothing to keep.

A note on how this guide was verified.
The build machine has the **OpenBSD**
netcat (Debian patchlevel 1.226-1ubuntu2),
and every captured command in these
chapters ran on it, against the lab, on
loopback — including the parts that went
wrong. Loopback UDP and Unix-domain
sockets both work on this machine, so
those chapters are captures, not
descriptions. Netcat's other dialects
(traditional `nc`, and Nmap's `ncat`) are
*not* installed here; chapter 12 is
honest about which of their differences
are documented rather than run. The full
ledger — what was captured, what was
only described, and the two surprises
(a resolver that answers *any* name, and
a caller who exited 0 without ever being
heard) — is in `criteria.md`.

## What this guide covers

- [**What netcat is**](what-netcat-is.md) —
  sockets in plain words, the permission
  rule, the lab, and what netcat is not
- [**Talking to a service**](talking-to-a-service.md) —
  netcat as a client: the banner, the
  echo, and reading `-v`'s one useful line
- [**HTTP by hand**](http-by-hand.md) —
  typing a web request yourself and
  reading everything the server says back
- [**Listening**](listening.md) — netcat
  as the server: the two-terminal chat,
  `-k`, and the one-caller-at-a-time truth
- [**Checking ports**](checking-ports.md) —
  `-z` and the exit code, refused versus
  silence, and when to put netcat down
  and pick up nmap
- [**Moving files**](moving-files.md) —
  one file across, in either direction,
  with the hash to prove it arrived
- [**Piping and scripts**](piping-and-scripts.md) —
  program output down a socket, and the
  exit code as the whole interface
- [**UDP**](udp.md) — datagrams: no
  connection, no promises, and the check
  that can only shrug
- [**Timeouts and hangs**](timeouts-and-hangs.md) —
  why netcat sits there, and `-N` and
  `-w`, the two ways of refusing to
- [**Unix sockets**](unix-sockets.md) —
  the same tool, no network at all
- [**The double edge**](the-double-edge.md) —
  why the admin's pocketknife is also the
  classic backdoor shape, and the habits
  that keep it on the admin side
- [**The netcat family**](variants.md) —
  OpenBSD, traditional, and ncat: whose
  flags you actually have
- [**Troubleshooting**](troubleshooting.md) —
  the silent failure, the hang, the caller
  nobody heard, and the resolver that lies
- [**Glossary**](glossary.md) — the terms,
  collected in one place

## What it doesn't cover

Real servers. Netcat listens like a
champ in a lab and serves one caller at
a time with no logging, no access
control, and no encryption — the
moment a listener matters, you want a
real daemon (and the guides for those
are elsewhere in this series). It also
doesn't cover port *scanning* beyond
the one-port check (that's nmap's
book), TLS by hand (ncat's `--ssl` is
named in chapter 12, not taught; use
the OpenSSL guide for the by-hand TLS
conversation), scripting netcat into a
daemon (`socat`, named in chapter 12,
is the tool built for that), or IPv6
beyond a mention — the lab is IPv4
loopback, and `-6` is one flag among
the variants.

## How to use this guide

Read chapter 1, start the lab
(`python3 examples/lab_server.py`, in
its own terminal), and keep a second
terminal open from chapter 2 on — most
of netcat only makes sense with a
terminal for each end of the wire.
Keep the lab afterwards: a service
whose answers you *know* is a standing
rehearsal for the day a real one's
behaviour surprises you.
