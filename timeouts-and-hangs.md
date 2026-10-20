# Timeouts and Hangs

Sooner or later every netcat user meets
the hang: the command was run, the
bytes were sent, and now terminal and
tool sit looking at each other. Nothing
is broken. Something is *waiting* —
and chapter 2 told you why: the two
directions are separate streets, and
netcat's default is to keep its street
open until the other side closes. The
fixture echoes and waits. You finished
typing and wait. Each is doing exactly
what it was asked.

The lab's demonstration, with a
lifeguard (`timeout`) so it can be
captured at all:

```
$ time (printf "hello\n" | timeout 3 nc 127.0.0.1 45002 >/dev/null)
# no -N, no -w: stdin ends, but nc stays on the line,
# waiting for the fixture, which is waiting for nc.
real	0m3.003s
```

stdin ended almost instantly; netcat
was still connected when the lifeguard
pulled it out at 3 seconds. That is
the whole mystery, and it has exactly
two cures, both measured below with
netcat timed directly (a pipeline's
clock measures its slowest member, so
these runs feed netcat from a file or
a held-open pipe instead):

```
nc -N   (input ends; -N says goodbye at once) : exit 0 after 0.0s
nc -w 2 (input ends; -w waits 2s for a reply)  : exit 0 after 2.0s
nc -w 2 (input held open but silent)           : exit 0 after 2.0s
```

## `-N`: say goodbye

`-N` answers the question "when am I
done?" with "when my input ends."
Netcat shuts down the sending side of
the socket — a proper protocol goodbye
— the peer sees end-of-input, finishes,
and closes; netcat exits. Measured:
**0.0s** after input. This is the flag
that makes transfers end (chapter 6),
makes receivers exit, and makes scripts
terminate. Its one contraindication: a
peer whose protocol says "the input
ending means *nothing*; my reply comes
when it comes." For those, leaving
`-N` off and waiting is correct — and
if the wait needs a bound, that's the
second cure.

## `-w`: bound the silence

`-w seconds` is netcat's patience: if
the connection sits idle — no bytes
either way — longer than that, netcat
leaves. Both measurements above show
its character:

- After input ended, `-w 2` granted
  the fixture 2.0s to say anything
  more, then exited cleanly (exit 0 —
  a timeout here is a *plan*, not an
  error).
- With input held open but silent —
  the terminal user who connected and
  then just sat there — the same 2.0s
  of mutual silence ended it.

`-w` also bounds the *connect* itself:
chapter 5's silent-port check only
terminated politely because `-w 2`
said so. Rules of thumb measured by
this chapter: interactive use, your
own Ctrl-C is the timeout; scripts and
checks, `-w` always, with the number
chosen as "how long is a legitimate
silence in this protocol?" — 1–3
seconds covers most honest ones on a
LAN; a slow service finishing a long
answer is chapter 2's reason the
default is infinite, and why you
choose on purpose.

A relative worth naming: `-q seconds`
(on this OpenBSD nc) delays quitting
*after* input ends — the same
neighbourhood as `-N`, with a pause
first, for peers that need a beat
before the goodbye. It wasn't needed
in the lab; it's here so the flag
isn't a stranger in `nc -h`.

## Diagnosing someone else's hang

When a *script's* netcat hangs, read
it as a sentence about the peer: the
peer hasn't closed, because in its
protocol the conversation isn't over —
or because it died mid-sentence and
nothing told the socket. The fixes, in
the order mortals need them:

1. Sender forgot `-N` → receiver waits
   forever for the rest of the file.
2. Nobody set `-w` → any silence, from
   any cause, is forever.
3. The receiver is a plain `nc -l`
   that already served its one caller
   (chapter 4) → the sender isn't
   hanging, it's *refused*... unless
   it's queued in a backlog behind a
   call that never ends. Back to 1.

Check: connect to the fixture by hand
(`nc 127.0.0.1 45002`), type a line,
get the echo — then do nothing. That
stillness is the un-`-w` default,
working as specified. Ctrl-C is a
perfectly good timeout at a terminal;
the chapter exists for everywhere
else.
