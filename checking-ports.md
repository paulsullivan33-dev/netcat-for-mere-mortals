# Checking Ports

The question netcat answers fastest is
the one administrators ask daily: *is
anything listening on this port, on
that machine?* The flag is `-z`
(zero I/O): connect, report, hang up,
send nothing.

```
$ nc -zv 127.0.0.1 45002; echo "exit: $?"
Connection to 127.0.0.1 45002 port [tcp/*] succeeded!
exit: 0

$ nc -zv 127.0.0.1 45999; echo "exit: $?"
nc: connect to 127.0.0.1 port 45999 (tcp) failed: Connection refused
exit: 1
```

Port 45002 is the lab fixture; 45999 is
the lab's empty chair. Two different
answers, and the **exit code** is the
part that matters: 0 for "a program
accepted the connection," 1 for "no."
That makes the check script-shaped:

```
$ for p in 45002 45003 45999; do nc -z 127.0.0.1 $p && echo "$p open" || echo "$p not open"; done
Connection to 127.0.0.1 45002 port [tcp/*] succeeded!
45002 open
Connection to 127.0.0.1 45003 port [tcp/*] succeeded!
45003 open
45999 not open
```

Mortals should know two quirks of this
nc's reporting, both visible above:

- **Success talks even without `-v`.**
  In `-z` mode the `succeeded!` line
  prints anyway. It goes to stderr, so
  it doesn't pollute a pipe — but it
  does decorate your loop's output.
- **Failure is silent without `-v`.**
  No `failed:` line for 45999 in the
  loop — the only evidence is the exit
  code (and your `||` branch). Without
  `-v`, a refused connection and a
  typo'd address look exactly alike:
  nothing, and a 1. When a check
  surprises you, re-run it with `-v`
  and let netcat explain itself.

## Three answers, not two

"Not open" is two different situations
wearing one exit code:

| Answer | Message (with `-v`) | What it proves |
|---|---|---|
| Open | `... succeeded!` | A program accepted the connection |
| Refused | `failed: Connection refused` | The machine answered and said *nothing listens here* — a fast, positive no |
| Silence | `timed out: Operation now in progress` | *Nobody answered at all* — your knock, or the reply, was dropped on the way |

The lab manufactured the third answer
honestly: a listener *was* running on
45001, behind a firewall rule that
drops its traffic without replying:

```
$ sudo iptables -A INPUT -p tcp --dport 45001 -j DROP
$ nc -zv -w 2 127.0.0.1 45001; echo "exit: $?"
nc: connect to 127.0.0.1 port 45001 (tcp) timed out: Operation now in progress
exit: 1
```

Same exit code as refused — the
difference is the message, and the
wait: refused comes back at once,
silence makes you wait out the whole
`-w`. (Without `-w 2`, a silent target
can keep you waiting for the operating
system's own connect timeout, which is
measured in minutes, not seconds. For
checks, `-w` is not optional.)

This is the diagnostic that earns
netcat its pocket space: **the port is
alive behind the firewall story.** A
service team says "it's up"; your
application says it can't connect; one
`nc -zv` from the right vantage point
tells you which third of the world is
wrong — service down (refused from its
own machine), firewall eating it
(silence from yours, success from
theirs), or fine (success from yours,
and the bug is in the application).

## When to put netcat down

Netcat checks the port you name. It
will not find the port you *typo'd*,
survey the machine, or test fifty
ports politely — the loop above is a
shell doing that, one process per
port, and it gets silly fast. The
hand-over:

- **One port, one machine, one
  question** — netcat. Especially from
  inside the environment with the
  problem: a container, a fresh VM, a
  machine with nothing installed.
- **"What is this machine exposing?"**,
  ranges, whole networks, version
  detection — nmap, whose book is this
  guide's sibling. Nmap also knows the
  difference this chapter taught (open /
  closed / filtered) and reports it as
  a first-class state for thousands of
  ports at once.

Check: with the lab running,
`nc -zv 127.0.0.1 45002` succeeds and
`nc -zv 127.0.0.1 45999` refuses. Stop
the fixture and re-run the first: the
answer changes to refused — the port
didn't move, the *program* left. That
difference, port versus program, is
the whole chapter.
