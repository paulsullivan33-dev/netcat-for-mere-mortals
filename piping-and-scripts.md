# Piping and Scripts

A file is one thing a pipe can carry.
The other everyday thing is a program's
output, delivered live — the "phone
home with a report" pattern. The lab's
receiving side waits with a file open;
the sending side pipes a small system
report:

```
$ nc -l 127.0.0.1 45001 > report.txt &     # receiving side
$ { uname -a; echo; df -h /; } | nc -N 127.0.0.1 45001

--- what landed in report.txt on the receiving side: ---
Linux htch-runtime 7.0.0-39-generic #1 SMP PREEMPT_DYNAMIC Thu Sep 24 08:42:15 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux

Filesystem      Size  Used Avail Use% Mounted on
overlay         7.5G  200M  7.3G   3% /
```

That's the pattern entire monitoring
hacks are made of: a cron job or a
human pipes a command's output at a
listening netcat, and a file appears on
the other machine. Netcat contributed
the wire and nothing else — no agent,
no account, no format. (The machine
name and figures above are the build
machine's own; the shape is the lesson.)

## The ingredients that make it a tool, not a trick

- **`-N` on the sender.** It's what
  turns "some output was sent" into
  "the report is complete and the
  receiver's netcat has exited, closing
  the file." Without it the receiver
  can't tell "report done" from
  "report still coming" — chapter 9.
- **The exit code is the interface.**
  A script can't read netcat's mind;
  it reads `$?`. The values this guide
  has measured on this nc:

  | Exit | Meaning |
  |---|---|
  | 0 | The socket did its job: connected, transferred, closed |
  | 1 | The connection failed — refused, timed out, name didn't resolve |
  | 0 (trap) | UDP send to nobody, or TCP into a busy listener's backlog: the socket "worked," no program ever saw your bytes (chapters 4 and 8) |

  That third row is why honest scripts
  verify the *effect* (the file exists,
  its hash matches, the report is in
  the file) rather than trusting `0`.

- **Silence is the default.** Without
  `-v`, errors print nothing at all.
  In a script that's cleanliness; in a
  log it's a hole. Give scripted checks
  `-v` and capture stderr to the log,
  or accept that your only evidence is
  the exit code you remembered to test.

## One-shot, on a schedule, beats standing around

A standing `nc -k -l` receiver is fine
for a lab afternoon. For anything
longer-lived, the mortal pattern is
one-shot both ends: a cron job on the
receiving machine starts a single
`nc -l` moments before the sender's
cron job sends, both exit, and nothing
listens in between. No daemon to
supervise, no port standing open all
week — and a failure mode (the report
simply isn't there) that's checked by
the file's existence, not by process
watching. The tools for the scheduling
half live in this series' systemd and
cron material; netcat's half is just
the two commands above, unchanged.

## Piping *in* the other direction

The mirror image also works: a program
can *consume* what netcat receives —
`nc -l ... | tar xf -` is the
old-timer's way to receive a directory
as a stream, and `nc ... | sh` is the
same shape wearing its chapter-11 face:
**a pipe into a shell executes whatever
arrives.** It appears in this guide
exactly once, here, labelled: on your
own machine, with input you produced,
it's a power tool; pointed at anything
else, it's the backdoor pattern itself.
Don't build that. The legitimate
receiving patterns in this guide end
at files.

Check: run the report pipeline twice.
The receiver (without `-k`) exits
after the first delivery — your second
send gets exit 1, connection refused,
because the ear left with the first
report. That's one-shot semantics
working as designed; `-k` is the
difference, and choosing between them
is choosing whether "receiver not
running" is a state you want to be
possible.
