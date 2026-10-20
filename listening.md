# Listening

Turn netcat around and it becomes the
other end of the wire: with `-l` it
*listens* — claims a port and waits for
whoever connects. One command is a
whole server:

```
$ nc -l 127.0.0.1 45001
```

Run that in one terminal, and in a
second terminal connect to it:

```
$ nc 127.0.0.1 45001
```

Now type. Whatever either side types
appears on the other's screen. There is
no protocol, no handshake greeting, no
names — the original chat program, two
terminals and a socket. Here is the
lab's run of it, captured with the two
ends' streams separated so you can see
which bytes crossed (on a real terminal
each side sees one merged stream: the
other's lines arriving, its own lines
as it types them):

**The listening terminal:**

```
$ nc -v -l 127.0.0.1 45001
Listening on localhost 45001
Connection received on localhost 37846
client: here. this is the whole protocol: text.
client: bye
```

**The connecting terminal:**

```
$ nc -v -N 127.0.0.1 45001
Connection to 127.0.0.1 45001 port [tcp/*] succeeded!
listener: anyone there?
```

Details worth keeping:

- `Listening on localhost 45001` is
  netcat confirming the port is claimed.
  If the port were taken, you'd get an
  error here instead — chapter 13.
- `Connection received on localhost
  37846` names the caller's *source
  port* — the return address half of
  the socket pair. Every connection has
  two ends, and each end is an
  address:port pair; 37846 is just the
  number the caller's OS picked for its
  end.
- When the client hung up, the listener
  exited (code 0). **A plain `nc -l`
  serves exactly one connection, then
  quits.** That sentence is load-bearing
  for the rest of the chapter.

## Staying up: `-k`

```
$ nc -k -l 127.0.0.1 45001
```

`-k` (keep listening) turns the
one-call ear into a standing one. The
lab pointed two separate callers at a
single `-k` listener:

```
$ nc -k -l 127.0.0.1 45001 &
$ printf "first visitor\n" | nc -N -w 2 127.0.0.1 45001
$ printf "second visitor\n" | nc -N -w 2 127.0.0.1 45001

--- what the one listener received from both: ---
first visitor
second visitor
listener state after both visitors: still listening
```

Both messages landed in the same
listener, in order, and it was still
listening afterwards (the lab stopped
it by hand). This is the shape of every
quick-and-dirty receiver in the later
chapters: one `nc -k -l` collecting
whatever's sent to it.

## The truth about "at the same time"

`-k` serves callers *in turn*, not
*together* — and even that phrasing is
generous. The lab held caller A on the
line with a plain (no `-k`) listener,
then had caller B try during A's call:

```
$ printf "caller B: hello?\n" | nc -w 2 127.0.0.1 45001
caller B exit: 0
--- what B received: ---
(nothing)

--- what the listener received, total: ---
caller A: I am on the line
```

B's line never arrived — and B exited
**0** anyway. What happened: the
operating system completed B's TCP
handshake into the listener's *backlog*
(the waiting room for connections the
program hasn't accepted yet), so B's
netcat honestly believed it had
connected and sent its line into the
socket. But the listening netcat was
busy being A's server; when A hung up,
it exited, the waiting room was swept
out, and B's queued connection — and
its unsent-in-effect line — were
dropped.

Two lessons, both permanent:

1. **Exit 0 means the socket worked,
   not that anyone heard you.** Delivery
   to a backlog is not delivery to a
   program. Any script that treats
   "nc exited 0" as "the message
   arrived" has this bug in it,
   whether its author knows it or not.
2. **Netcat is a one-conversation
   tool.** Real servers accept in a
   loop and handle callers concurrently,
   with logging and limits. The day you
   need that, you've outgrown the ear
   and want a daemon — or, for receiving
   files and reports, the scheduled,
   one-shot patterns of chapter 7
   instead of a standing listener.

Check: run the chat with `-v` on the
listener, as above, and note the source
port in `Connection received`. Connect
a second time (you'll need `-k`) — the
source port changes. The listener's
address:port is the stable half of the
pair; the caller's port is per-call.
