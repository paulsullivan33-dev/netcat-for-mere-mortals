# What Netcat Is

**Netcat** is a small command-line tool
for making raw network connections — and
for being the other end of one. You give
it an address and a port; it opens the
connection (or waits, listening, for
someone else to open one to you) and
then passes bytes: what you type goes
out, what arrives gets printed. It does
not know or care whether those bytes are
a web page, a mail conversation, or two
people typing at each other. Network
people have called it "the TCP/IP Swiss
army knife" for thirty years; a plainer
description is that it is the network
equivalent of picking up a telephone
handset with no dial, no directory, and
no manners built in.

## The one idea: a socket

Every network conversation happens
through a **socket** — an endpoint your
operating system gives a program, the way
it gives a program an open file. The
resemblance is not a metaphor: a program
*reads* from a socket and *writes* to
it, much as it reads and writes files.
A socket is named by an **address** and
a **port**: the address says which
machine (127.0.0.1 is "this machine," the
**loopback** address), and the port says
which program on that machine — a number
from 1 to 65535 that the receiving
program has claimed by *listening* on
it.

Most tools hide the socket behind a
protocol. Your browser knows it wants a
web page, so it speaks HTTP for you.
Netcat hides nothing, because it speaks
nothing. It hands you the socket itself:

- Everything you type (its **stdin**)
  goes down the socket, byte for byte.
- Everything that arrives comes to your
  screen (its **stdout**), byte for byte.

That is the entire tool, and it is why
netcat teaches things browsers can't:
when *you* are the protocol, you see
exactly what the protocol is made of.

## The rule

Netcat connects to things and listens
for things. Both powers are easy to
point at the wrong target, and a
listening socket is — as chapter 11
discusses at length — exactly the shape
of a classic backdoor. So this guide's
rule is the one its nmap sibling
states on its first page:

> **Only connect to, and listen on,
> machines and networks you own or
> administer — or have explicit
> permission to use.**

Everything in this guide happens on
127.0.0.1, where the rule is free to
keep: the only machine you can possibly
bother is your own.

## The lab

One fixture, in `examples/`:

```
$ python3 examples/lab_server.py --check
banner+echo fixture: tcp/45002 on 127.0.0.1
banner: LabEcho/1.0 -- a lab fixture: it says hello, then repeats you.
deliberately closed specimen: tcp/45999 (nothing binds it)
```

Run without `--check`, the fixture
listens on tcp/45002. It greets every
caller with one line — its **banner** —
and then repeats back whatever it
receives, line for line. It is not SSH,
not HTTP, not anything with an entry in
the phone book of well-known ports; it
is a machine that says hello and
repeats you, which is all a netcat lab
needs. Alongside it, the guide uses
Python's built-in web server on
tcp/45003 (for chapter 3), netcat
listening to itself on tcp/45001, and
one deliberately empty chair: port
45999, where nothing listens, because a
genuine refusal is a lesson too.

Check: with the fixture running
(`python3 examples/lab_server.py` in
its own terminal), chapter 2's first
command gets its banner back. If it
doesn't, the fixture's terminal will
say why — start there, not with netcat.

## Have you got it — and which one?

Netcat has a family problem the later
chapters keep meeting: the name `nc`
covers several different programs whose
flags overlap but do not match. The
build machine's is:

```
$ nc -h 2>&1 | head -3
OpenBSD netcat (Debian patchlevel 1.226-1ubuntu2)
usage: nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
	  [-m minttl] [-O length] [-P proxy_username] [-p source_port]

$ dpkg-query -W netcat-openbsd
netcat-openbsd	1.226-1ubuntu2
```

Every capture in this guide ran on this
**OpenBSD** netcat, the common
denominator on modern Linux and the
BSDs, and the guide teaches that dialect
as the core. Chapter 12 maps the
differences that matter — the
traditional netcat still shipped by some
systems, and `ncat`, the Nmap project's
netcat, which is *not* installed here:

```
$ command -v nc ncat
/usr/bin/nc
```

Downloaded for Windows, `nc.exe` exists
in third-party builds of varying
trustworthiness; if you didn't build it
or get it from your OS vendor, don't run
it. macOS ships an OpenBSD-derived `nc`
whose flags are close to — not identical
with — the ones here. The commands in
this guide are Linux captures; the ideas
transfer, a few flags don't, and
chapter 12 says which.

## What netcat is not

- **Not a scanner.** It checks one port
  the way you knock on one door. For the
  census — what is listening on this
  machine, on this network — you want
  nmap, and chapter 5 says exactly where
  the hand-over point is.
- **Not a server.** It will listen, and
  chapter 4 makes it chat. But it serves
  one caller at a time, logs nothing,
  authenticates nobody, and encrypts
  nothing. A fine ear; a terrible
  butler.
- **Not safe company by default.** The
  connection is plaintext and the
  listener is unauthenticated: anyone who
  can reach the port is the peer. The
  lab binds everything to 127.0.0.1 for
  this reason, and chapter 11 is the
  long version.
