# The Netcat Family

Everything captured in this guide ran
on one program: the **OpenBSD netcat**,
Debian patchlevel 1.226-1ubuntu2. It is
not the only program called `nc`, and
the differences are the kind that waste
an afternoon — a script written against
one dialect failing, quietly or loudly,
on another. This chapter is the map.
Its first half is checkable against
your own `nc -h`; the parts about
programs *not installed on the build
machine* are labelled as documented,
because the series rule is that a
capture beats a claim, and here there
are no captures to be had:

```
$ command -v nc ncat
/usr/bin/nc
```

## The three dialects

**OpenBSD netcat** — this guide's.
The default `nc` on Debian, Ubuntu,
the BSDs, and (a close relative) macOS.
Written to be small, careful, and
complete for hand use: `-N`, `-k`,
`-U`, `-w` all as taught here, and —
chapter 11's point — deliberately **no
`-e`**.

**Traditional netcat** — the 1990s
original by Hobbit, kept alive in the
`netcat-traditional` package and still
the `nc` on some older and embedded
systems. Documented differences that
bite: it listens with a separate `-p`
(`nc -l -p 45001`, where OpenBSD wants
the port as an argument), it has **no
`-N`** (its goodbye manners are
different, which retro-fits chapter 9's
hang with a different shape), no `-k`,
no `-U` — and it *does* have `-e`,
the execute-on-connect flag that made
it the backdoor era's tool of choice.
If a tutorial's netcat commands look
almost-right and fail, this dialect
swap is the usual explanation.

**ncat** — the Nmap project's netcat,
a ground-up rewrite that ships *with
nmap* on some distributions and as its
own package on others. Documented
extras, named here and not taught as
common core, because they aren't:
`--ssl` (TLS on the connection — the
family's one built-in answer to
chapter 3's HTTPS silence), `--broker`
(one listener, many callers, messages
relayed — the thing chapter 4 admits
netcat can't do), `--chat`, access
control lists, and proxy support. Where
ncat exists, it's a fine tool; where a
script must run on whatever `nc` a
strange machine happens to have,
OpenBSD's core — connect, listen,
`-z`, `-w`, files through stdin and
stdout — is the portable subset.

## Flags: whose are whose

| Flag | OpenBSD (taught) | Traditional | ncat |
|---|---|---|---|
| `-l` listen | yes | yes (with `-p`) | yes |
| `-z` check only | yes | yes | yes |
| `-v` verbose | yes | yes | yes |
| `-u` UDP | yes | yes | yes |
| `-w` timeout | yes | yes | yes (`--wait`) |
| `-N` shutdown after input | yes | **no** | no (spelled `--send-only`) |
| `-k` keep listening | yes | no | yes |
| `-U` Unix sockets | yes | no | yes |
| `-e` run a program | **no (by design)** | yes | yes (`--exec`) |
| TLS | no | no | yes (`--ssl`) |

Read the table as this guide's claims
policy in miniature: the OpenBSD column
is captured; the other two columns are
the projects' documented behaviour,
summarised so you can recognise a
strange dialect in the wild — run
`nc -h` on any new machine before
trusting a script there, because the
usage line tells you which family
you're holding (and, on the build
machine, told us in chapter 1).

## The bigger cousin

One name to know without a chapter:
**socat**, installed on more machines
than you'd expect, is netcat's idea
grown into a general-purpose relay —
sockets to files to serial ports to
TLS, with forking and options to
match. When a job outgrows netcat
(chapter 4's concurrency wall, chapter
11's encryption gap), socat is usually
the next shelf, and everything this
guide taught about the two directions
of a socket still applies there.

Check: on any machine new to you,
`nc -h 2>&1 | head -1` names the
dialect. Compare it with chapter 1's
capture before reusing a command from
memory — especially a listener's port
syntax, which is where the dialects
draw blood first.
