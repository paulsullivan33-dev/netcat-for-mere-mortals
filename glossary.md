# Glossary

**backlog** — The operating system's
waiting room for connections a
listening program hasn't accepted yet.
The handshake completes into the
backlog, which is why a caller can
"connect" — and even exit 0 — without
the program ever knowing (chapter 4).

**banner** — The greeting some
services send the moment a connection
opens: a line of text naming (or
claiming) the service. Reading it
costs no protocol knowledge and proves
something is listening (chapter 2).

**datagram** — One UDP packet,
addressed and sent on its own: no
connection, no handshake, no goodbye.
A letter, not a phone call
(chapter 8).

**exit code** — The number a program
leaves behind for whoever ran it
(`$?` in shell). Netcat's contract:
0 when the socket did its job, 1 when
the connection failed — with two
honest traps (backlog delivery, UDP
to nobody) where 0 doesn't mean
anyone heard you (chapters 4, 7, 8).

**FIN** — TCP's polite goodbye: the
signal that a side has finished
sending. Netcat's `-N` sends it when
your input ends (chapter 9).

**handshake (TCP)** — The three-step
opening of every TCP connection:
SYN, SYN-ACK, ACK. Until it completes
there is no connection — only, at
most, a backlog entry (chapter 4).

**ICMP port unreachable** — The
machine's own "nobody here" reply to
a UDP packet. Loopback delivers it
honestly; networks often filter it,
which is why UDP checks shrug
(chapter 8).

**listener** — A program that has
claimed a port and waits for
connections on it. `nc -l` is one;
every real server contains one
(chapter 4).

**loopback** — The address range
(127.0.0.1 and friends) that means
"this machine." Traffic to it never
leaves the box, which is why the
whole lab lives there (chapter 1).

**port** — A number, 1–65535, naming
which program on a machine a socket
is for. Claimed by listening; answered
for by whoever listens (chapter 1).

**socket** — An endpoint for a
network conversation, handed to a
program the way an open file is:
you read from it and write to it.
An address plus a port names one
(chapter 1).

**stderr / stdin / stdout** — A
program's three standard streams:
input, output, and the side channel
for its own voice. Netcat sends data
to stdout and puts its reports
(`Connection to... succeeded!`) on
stderr, which is why `-v` never
pollutes a transfer (chapter 2).

**Unix-domain socket** — A socket
whose address is a file path instead
of a port, for programs on one
machine. Guarded by file permissions;
its socket file outlives its listener
(chapter 10).

**zero I/O (`-z`)** — Netcat's check
mode: connect, report, hang up, send
nothing. The one-port question,
answered by the exit code
(chapter 5).
