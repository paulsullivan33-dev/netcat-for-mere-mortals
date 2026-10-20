# Troubleshooting

Every symptom here happened in the lab,
to the person building it or on purpose.
The format is the series' usual:
symptom → what it actually means → the
fix.

## It connects, I send, and then it just sits there

**Meaning:** the conversation isn't
over — your side finished *sending*
but never said goodbye, and the other
side is waiting for the rest. Netcat's
default is to stay on the line after
stdin ends (chapter 9).

**Fix:** `-N` on the sending side, so
end-of-input shuts down the socket's
sending half; or `-w` to bound the
silence. Measured difference: with
`-N`, exit 0 in 0.0s after input; with
neither, the lab's run was still
sitting there when its lifeguard
pulled it out at 3s — and would be
still.

## The command failed and printed nothing at all

**Meaning:** it didn't fail quietly on
purpose; without `-v`, this netcat
prints *nothing* on failure — no
message, just exit 1. A refused
connection, a bad address, and a
mistake all look identical: silence.

**Fix:** re-run with `-v`. The failure
names itself:

```
$ nc -zv 127.0.0.1 45999; echo "exit: $?"
nc: connect to 127.0.0.1 port 45999 (tcp) failed: Connection refused
exit: 1
```

In scripts, either always use `-v` and
log stderr, or treat the exit code as
the entire report and design for that
(chapter 7).

## The check says timed out — but the service is up

**Meaning:** silence, the third answer
(chapter 5). Something between you and
the service — usually a firewall doing
DROP, not REJECT — is eating the
packets. The tell is the wait: refused
answers instantly; silence makes you
wait out your whole `-w`.

**Fix:** run the same `nc -zv` from the
service's own machine (loopback). If
it succeeds there and times out from
yours, the service is innocent and the
path is guilty. If you'd run the check
without `-w`, you'd still be waiting —
the operating system's connect timeout
is minutes long.

## My message was sent and nc exited 0, but nothing arrived

**Meaning:** your bytes were delivered
to a socket nobody was reading — the
classic case is chapter 4's: the
listener was busy with (or still
finishing) another caller, your
connection waited in its backlog, and
the listener quit before accepting
you. UDP has the purer version
(chapter 8): sending to an empty port
exits 0 because UDP cannot know.

**Fix:** there isn't a flag for "make
sure a program read it" — that
knowledge lives one level up. Have the
receiver acknowledge (a reply, a file,
a log line), or make the receiving side
`-k` and long-lived enough that "busy"
can't happen. Design scripts to verify
the *effect*, not the exit code.

## The file arrived short — or the receiver's file is empty

**Meaning, empty receiver file:** the
sender never connected (chapter 6's
silent exit 1 creates a 0-byte file via
your own redirection). Empty means
*never started*, not *corrupted*.

**Meaning, short file:** the stream
was cut — sender killed before
finishing, or sent without `-N` and
someone lost patience with the hang
and Ctrl-C'd whichever side was in
front of them.

**Fix:** hashes, both ends, every time
(chapter 6). If they differ, redo the
transfer; netcat has no resume, and a
partial file with a confident name is
worse than none.

## The name resolved and the check "succeeded" — for a host that doesn't exist

**Meaning:** your resolver is lying to
you. The lab's build machine does
this:

```
$ nc -zv no-such-host.invalid 45002; echo "exit: $?"
Connection to no-such-host.invalid (198.18.83.181) 45002 port [tcp/*] succeeded!
exit: 0

$ getent hosts no-such-host.invalid; echo "exit: $?"
198.18.83.181   no-such-host.invalid
exit: 0
```

The sandbox's resolver answers *any*
name with an address in a
reserved-for-testing range, and
something there accepts connections.
Real-world versions are commoner than
you'd hope: ISP resolvers that turn
typos into search pages, captive
portals, wildcard DNS on a domain you
typo'd *into*. **Fix:** when a result
is too good, check the name
independently (`getent hosts`,
`dig`) and distrust any environment
that answers everything — a check
that cannot fail cannot inform.

## The Unix socket listener won't start — the path is "in use"

**Meaning:** chapter 10's leftover —
the socket file from the last listener
is still on disk, because exiting
doesn't remove it.

**Fix:** `rm` the stale socket file,
then start the listener. And build the
habit at the source: lab sockets live
in a scratch directory you clean as a
set.

## The commands from a tutorial don't work

**Meaning:** the tutorial's `nc` isn't
yours. The flag alphabets overlap
without matching — most famously, a
traditional-netcat listener wants
`nc -l -p PORT` while OpenBSD wants
`nc -l HOST PORT`, and `-N` doesn't
exist on the traditional one at all.

**Fix:** `nc -h 2>&1 | head -1` on
the machine in front of you, and
chapter 12's table. Ten seconds of
identification saves the afternoon of
guessing.

Check: each fix above can be rehearsed
against the lab in minutes — and the
lab is the place to meet these for the
first time, rather than at 3 a.m. with
a production-shaped socket.
