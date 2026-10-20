# UDP

Everything so far was TCP: connections,
handshakes, refusals, goodbyes. With
`-u`, netcat switches to **UDP** — and
gives most of that back. A UDP packet
(a **datagram**) is a letter dropped in
a mailbox: no connection is opened, no
handshake confirms the address exists,
no goodbye closes anything. Netcat's
job shrinks to addressing the envelope
and, on the listening side, catching
whatever arrives.

The lab's exchange, on loopback:

```
$ nc -u -l 127.0.0.1 45004            # listening side (UDP this time)
$ printf "a datagram says hello\n" | nc -u -N -w 1 127.0.0.1 45004

--- what the listening side received: ---
a datagram says hello
```

That's a complete UDP conversation:
one datagram, delivered, no ceremony.
Note what the listening side had to
bring that TCP didn't ask for — a
`timeout` in the lab harness. A TCP
listener knows when a call is over;
a UDP listener hears a datagram and
then... silence that could mean
"finished" or "more coming." UDP
netcat sessions end by timeout
(`-w`), by Ctrl-C, or by giving up,
never by the protocol saying so.

## The check that can only shrug

Chapter 5's `-z` works for UDP too —
after a fashion. Against a listener
that is genuinely up:

```
$ nc -zuv -w 2 127.0.0.1 45004; echo "exit: $?"
Connection to 127.0.0.1 45004 port [udp/*] succeeded!
exit: 0
```

And against an empty port, on this
loopback:

```
$ nc -zuv -w 2 127.0.0.1 45998; echo "exit: $?"
exit: 1
```

Read the fine print before trusting
either line. The "succeeded" is really
"nothing said no": netcat sent a probe
and heard no complaint. The failure
owes its honesty to loopback — the
machine itself answered the probe with
an ICMP "port unreachable," because on
one machine nothing filters it away.
Out on a real network, firewalls eat
unreachables as happily as they eat
probes, and the same check against a
dead port returns the living port's
answer: silence, read as success. This
is exactly nmap's `open|filtered`
shrug, wearing a smaller hat, and it's
why the nmap guide treats UDP states
with tongs. A UDP `-z` can sometimes
tell you *no*; it can only ever
*suggest* yes.

## The send that cannot fail

The mirror-image lesson, sending a
whole datagram (not a `-z` probe) to
the empty port:

```
$ printf "is anyone there?\n" | nc -u -w 2 127.0.0.1 45998; echo "exit: $?"
exit: 0
```

No error, exit 0. The datagram left;
UDP has no way to know nobody caught
it, and netcat faithfully reports that
non-knowledge as success. Compare TCP,
where the same send to the same kind
of emptiness gets an instant refusal
and exit 1. Any script that needs to
know a UDP message *arrived* must get
that knowledge from the application —
a reply datagram, a changed file —
because the protocol structurally
cannot provide it.

## When UDP is the right tool anyway

Protocols choose UDP when a lost
message is cheaper than a delayed one,
or when there's no "connection" to be
had: DNS lookups, DHCP, NTP time,
voice, game state — and netcat's `-u`
is how you poke those by hand and
watch your own UDP programs behave.
Inside this guide it's also the honest
limit of the pocketknife: netcat will
carry datagrams as happily as streams,
but it cannot lend them the guarantees
TCP had — and now you know precisely
which guarantees those were, because
you watched each one leave.

Check: repeat the `-zuv` pair with the
UDP listener stopped. On loopback the
"open" port's answer changes to the
same silent exit 1 as the closed one —
the ICMP unreachable starts arriving
for it too. Same command, same flags;
the answer changed because the
*machine's* behaviour did.
