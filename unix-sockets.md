# Unix Sockets

Not every socket lives on a network.
Programs on one machine often talk
through **Unix-domain sockets**:
sockets whose "address" is a file path
instead of an address:port pair. Your
container runtime, your database, and
half your desktop use them, because a
file path can be guarded by ordinary
file permissions in a way a port
cannot. Netcat speaks this dialect too,
with `-U` — and since it's the same
stdin/socket/stdout machine, everything
you've learned transfers.

The lab, on the build machine's disk:

```
$ nc -l -U lab.sock &          # listening side, started first
$ ls -l lab.sock
srwxrwx--- 1 root nogroup 0 Oct 20 19:24 lab.sock

$ printf "hello over a unix socket\n" | nc -N -U lab.sock; echo "exit: $?"
exit: 0

--- what the listening side received: ---
hello over a unix socket
```

The `s` at the front of `srwxrwx---`
is the file type: socket. It weighs 0
bytes — the file is a meeting point,
not a container; the bytes went through
the kernel, not into the file. And the
permissions are real: that socket is
readable/writable by its owner and
group only, which is why a database's
socket in a directory you can't read
is genuinely private, while its
loopback TCP port would be reachable
by every process on the machine.

One untidiness, captured honestly:

```
$ ls -l lab.sock    # after the listener exits
srwxrwx--- 1 root nogroup 0 Oct 20 19:24 lab.sock
```

**The socket file stays behind** when
the listener exits. Nothing cleans it
up for you; a stale socket file is the
Unix-socket equivalent of a port that's
"in use" by a ghost — the next listener
on that path can fail until you
`rm` the file, and chapter 13 lists it
as a symptom. Mortal habit: socket
paths for experiments live in your
scratch directory, and you delete them
with the rest of the lab.

Where this earns its keep beyond the
lab: asking a daemon that only listens
on a socket whether it's alive, and
how it answers — container runtimes,
databases, and system services all
expose one, and `nc -U` is the one-liner
that talks to them with the same hands
you've used all guide. (Protocols over
Unix sockets are usually the same text
shapes — an HTTP conversation can
travel over one unchanged.)

Check: chapter 5's port check works
here too, with no network involved —
and one reporting quirk of its own:

```
$ nc -zvU lab.sock; echo "exit: $?"   # listener is up
exit: 0

$ nc -zvU no-such.sock; echo "exit: $?"
nc: /home/hatch/workspace/netcat-lab/work/no-such.sock: No such file or directory
exit: 1
```

Success is *silent* this time (no
`succeeded!` line, TCP-style) — exit 0
is the whole report — while a missing
socket file gets a named error. Proof,
if any were needed, that the check was
never really about the network. It was
about whether a program is there.
