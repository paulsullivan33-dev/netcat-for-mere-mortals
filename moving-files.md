# Moving Files

Because a socket is just stdin in one
direction and stdout in the other, a
file transfer is two redirections
facing each other. The lab's payload is
the shipped specimen, copied 200 times
so there's enough of it to matter:

```
$ wc -c payload.txt; sha256sum payload.txt
49200 payload.txt
4269a2a243bb386ef678ed333ab20b3db7c16f3ae16a776f2b5072879f23baf2  payload.txt
```

## Push: sender connects to a waiting receiver

```
$ nc -l 127.0.0.1 45001 > received.txt &     # receiving side, started first
$ nc -N 127.0.0.1 45001 < payload.txt; echo "sender exit: $?"
sender exit: 0

$ wc -c received.txt; sha256sum received.txt
49200 received.txt
4269a2a243bb386ef678ed333ab20b3db7c16f3ae16a776f2b5072879f23baf2  received.txt

$ cmp payload.txt received.txt && echo IDENTICAL
IDENTICAL
```

The order of operations is the whole
technique: the **receiver starts
first** and waits; the sender connects,
streams the file, and `-N` gives the
receiver the end-of-file signal that
makes its netcat exit and close
`received.txt`. Then the proof, which
is not optional: same byte count, same
SHA-256, and `cmp` silent — byte for
byte identical.

## Pull: the file waits, the receiver comes to it

```
$ nc -l 127.0.0.1 45001 < payload.txt &     # serving side: whoever connects gets the file, once
$ nc -N -w 3 127.0.0.1 45001 > pulled.txt; echo "receiver exit: $?"
receiver exit: 0

$ sha256sum payload.txt pulled.txt
4269a2a243bb386ef678ed333ab20b3db7c16f3ae16a776f2b5072879f23baf2  payload.txt
4269a2a243bb386ef678ed333ab20b3db7c16f3ae16a776f2b5072879f23baf2  pulled.txt

$ cmp payload.txt pulled.txt && echo IDENTICAL
IDENTICAL
```

Same file, opposite initiative. This
direction reads naturally ("the file is
*on* that machine; go get it") and has
the sharpest edge in the chapter,
stated plainly in the comment: the
serving netcat hands the file to
**whoever connects first**, once, and
exits. No password, no names, no "are
you sure." On loopback that's a lab.
On a network it's a giveaway — see
chapter 11 before you serve anything
this way anywhere else.

## When nobody is listening

```
$ nc -N -w 3 127.0.0.1 45001 > nothing.txt; echo "exit: $?"   # nobody is listening this time
exit: 1
$ wc -c nothing.txt
0 nothing.txt
```

Silent (no `-v`), exit 1, and an empty
file created by your own redirection —
not by netcat. The receiver-side moral:
**an empty output file means the
transfer never started**, and the
sender-side moral is chapter 5's:
without `-v`, failure says nothing; the
exit code is the witness.

## What this is not

Netcat file transfer is a party trick
with real uses (next chapter and
chapter 11), and its limits are part of
the trick:

- **No resume.** A connection that dies
  at 90% delivers a 90% file and
  starts over from nothing. `rsync`
  exists because of this sentence.
- **No encryption, no integrity
  built in.** The bytes are plaintext
  on the wire, and the only proof of
  arrival is the hash *you* run. (On
  loopback, plaintext is a fact; on a
  network, it's a decision — chapter 11.)
- **No directories, no metadata.** One
  stream of bytes: no filename, no
  permissions, no timestamps cross the
  wire. The name `received.txt` was
  chosen by the receiving command, not
  sent by the sender.
- **The sender doesn't know you got
  it all.** Exit 0 means the bytes
  left. The hash comparison is the
  *only* "it arrived" in the system.

Check: after either transfer,
`sha256sum` on both ends must print the
same string, and `cmp` must say nothing
at all. If the hashes differ, believe
them, not the exit codes — the usual
cause is a transfer cut short (chapter
8's missing `-N`, or a receiver started
late), and the fix is to redo it, not
to trust the partial file.
