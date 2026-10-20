# Talking to a Service

The simplest thing netcat does is also
the one you'll use most: connect to a
service and have the conversation
yourself. Start the lab fixture
(`python3 examples/lab_server.py`, its
own terminal), then, in yours:

```
$ { printf "hello fixture\n"; sleep 0.3; printf "second line\n"; sleep 0.3; } | nc -v -N 127.0.0.1 45002
Connection to 127.0.0.1 45002 port [tcp/*] succeeded!
LabEcho/1.0 -- a lab fixture: it says hello, then repeats you.
hello fixture
second line
exit: 0
```

(The pipes and `printf`s are this
guide's way of typing on your behalf so
the exchange can be captured. At your
own terminal you would run plain
`nc -v 127.0.0.1 45002` and type the two
lines yourself, ending with Ctrl-C or
Ctrl-D. What crossed the wire is
identical either way.)

Read the capture in the order the bytes
moved:

1. **`Connection to 127.0.0.1 45002 port
   [tcp/*] succeeded!`** — netcat's own
   voice, not the fixture's. It goes to
   **stderr**, which is why it appears
   even though stdout was the pipe's
   business. `-v` (verbose) buys this
   line; it is the difference between
   "connected" and guessing. The
   `[tcp/*]` shrugs about the service
   name — netcat doesn't know what
   45002 is for, and says so honestly
   with a `*` instead of a guess.
2. **The banner.** The fixture speaks
   first, before receiving anything:
   one line naming itself. Many real
   services do this — SSH servers, mail
   servers, FTP servers all greet you —
   and reading the greeting is the
   oldest diagnostic there is: it proves
   *something* is listening, tells you
   what it claims to be, and costs no
   protocol knowledge at all.
3. **The echo.** Each typed line came
   back verbatim. The fixture is a
   mirror; real services would answer in
   their own protocol — which is the
   same experience, one level up: you
   send text shaped like the protocol,
   you read text shaped like the reply.

## The two directions are separate

A netcat session is two one-way streets
sharing a command:

- **stdin → socket:** what you type
  (or pipe, or redirect from a file) is
  sent.
- **socket → stdout:** what arrives is
  printed (or redirected to a file —
  chapter 6 lives on this).

Neither direction implies the other.
The fixture's banner arrived before
anything was sent. Your lines were sent
whether or not the fixture chose to
answer. Most netcat confusion — and the
whole of chapter 9's hang — is a
one-way street being mistaken for a
conversation that ended. Hold the two
directions apart in your head from here
on.

## Ending the call

The capture's `-N` told netcat: when
stdin ends, shut down the sending side
of the socket — say goodbye, properly,
in the protocol's own terms (a TCP FIN,
for the glossary). The fixture saw the
goodbye, closed its side, and netcat
exited 0. Without `-N`, netcat takes
stdin ending as "I have no more to
say" — *not* as "I am leaving" — and
stays on the line listening. Sometimes
that is what you want (you're waiting
for a slow service to finish answering).
Usually, at a terminal, you end a
session with Ctrl-C and never notice
the distinction. Chapter 9 is about
the times you do notice.

Check: connect to the fixture without
`-v` and the banner and echo still
work — only netcat's own `Connection
to...` line vanishes. The service can't
tell the difference; only you can.

## Talking to strangers (your own)

Everything the fixture did, real
services on your own machines will do:
a mail server on port 25 greets you
with its name and will chat in SMTP
commands; an SSH server on 22 greets
you with a version line and then
expects cryptography, so the
conversation politely goes no further.
Chapter 3 takes the most familiar
protocol of all — HTTP — and has the
whole conversation by hand, because
HTTP, alone among the famous protocols,
is text all the way down and will
therefore talk to a mortal.
