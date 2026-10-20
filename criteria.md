# Writing Criteria

Every guide in this repo is written to the same
standard. If you're adding or editing a guide —
human or AI — hold it to these.

1. **Plain words, real ideas.** Simple language,
   never dumbed-down concepts. Explain jargon on
   first use; collect terms in the glossary.
2. **No hype.** No marketing adjectives, no
   "revolutionary," no promises about what
   something will do for the reader.
3. **Honest about limits.** Say what the thing
   *can't* do. State uncertainty instead of
   smoothing it over. Validation notes include
   what remains unverified.
4. **No invented numbers.** Benchmarks, defaults,
   and specs are either measured or qualified with
   "depends on your setup." If it wasn't tested,
   say so.
5. **Checkable.** Commands are meant to be run,
   with "Check:" blocks showing what success looks
   like. Sources are linked, not asserted.
6. **Respect the reader's setup.** Call out
   Windows/Mac/Linux differences. Don't assume a
   GPU, a budget, or prior experience.
7. **Safety isn't skipped.** Real risks get
   stated plainly, not buried.
8. **Scoped.** Each guide says what it covers and
   points elsewhere for the rest. No guide
   pretends to be the whole subject.
9. **Structure over prose.** Tables, before/after
   examples, symptom → fix. Scannable beats essay.

## Verification notes for this guide

Standard 3 and 4 applied to this guide,
specifically. The build machine ran Ubuntu
24.04 as root, with **OpenBSD netcat
(Debian patchlevel 1.226-1ubuntu2)** already
installed (`netcat-openbsd 1.226-1ubuntu2`).
Every quoted output in the chapters is a
capture from that netcat, run against the
shipped lab on loopback. Working
transcripts are kept with the build
(`netcat-lab/transcripts/`, nineteen files).

**The lab.** `examples/lab_server.py`
stands up one fixture: a banner + echo
server on tcp/45002. Alongside it the
chapters use Python's built-in web
server on tcp/45003 serving
`examples/index.html`, netcat listening
to itself on tcp/45001, a stream
listener on udp/45004, a Unix socket in
the lab's scratch directory, and two
deliberate empty chairs: tcp/45999 and
udp/45998. The transfer payload is the
shipped `examples/specimen.txt`
concatenated 200 times (49,200 bytes,
sha256
`4269a2a243bb386ef678ed333ab20b3db7c16f3ae16a776f2b5072879f23baf2`).

**Live-captured (every command run for real on the build box):**

- The version/identity captures:
  `nc -h`'s first lines, `dpkg-query -W
  netcat-openbsd`, and `command -v nc
  ncat` — the latter returning only
  `/usr/bin/nc`, which is the evidence
  that ncat is absent here.
- The fixture's `--check` output, its
  banner, and its echo of two typed
  lines under `nc -v -N` (the
  `succeeded!` line, banner, both
  echoes, exit 0).
- HTTP by hand: `GET / HTTP/1.0`
  against the Python web server (full
  200 response, headers, specimen
  body) and `GET /no-such-page` (full
  404). The server's own log lines for
  those requests were also read back
  and match chapter 3's Check.
- The two-terminal chat, both sides:
  the listener's `Listening on` /
  `Connection received on localhost
  37846` lines and received text; the
  client's `succeeded!` line and
  received text; both exits 0.
- `-k` keeping one listener alive
  across two sequential callers (both
  messages received, listener verified
  still running, then stopped by hand).
- The backlog experiment: caller B
  connecting during caller A's call —
  B exit 0, B's line absent from the
  listener's total, listener exit 0
  after A hung up.
- Port checks: `-zv` open (exit 0) and
  refused (exit 1, message verbatim);
  the `-z` loop over three ports,
  including its two reporting quirks
  (success prints without `-v`;
  failure prints nothing without
  `-v`), each re-verified in a direct
  follow-up probe before the chapters
  described it.
- Manufactured silence: an iptables
  DROP rule on a port with a live
  listener produced the `timed out:
  Operation now in progress` message
  and exit 1; the rule was removed
  immediately after the capture and
  the empty chain re-verified.
- File transfers in both directions
  (49200 bytes; identical sha256 at
  both ends; `cmp` → IDENTICAL), and
  the nobody-listening pull (exit 1,
  silent, 0-byte file).
- The piped report (`uname -a` +
  `df -h /`) arriving whole at a
  listening netcat.
- UDP on loopback: a datagram
  delivered to a `nc -u -l` listener;
  `-zuv` against a genuinely live UDP
  listener (`succeeded!`, exit 0) and
  against a closed port (silent exit
  1, loopback's ICMP unreachable doing
  the work); a full UDP send to the
  closed port exiting 0 with no error.
  An earlier draft of this capture
  checked the port after its listener
  had already timed out and recorded a
  false "failure against a live
  listener"; the capture was re-run
  against a verified-live listener and
  the chapter follows the re-run.
- Unix sockets: `-l -U` listener, the
  `srwxrwx---` socket file, a delivered
  message, the socket file's survival
  after the listener exits, and
  `-zvU` (silent exit 0 live; named
  error + exit 1 for a missing path).
- Timeouts, measured with netcat timed
  directly (a pipeline's clock measures
  its slowest member — the lab's first
  measurements were of producers, not
  of netcat, and were discarded): the
  unflagged hang (still connected when
  `timeout` killed it at 3s); `-N`
  exit 0 after 0.0s; `-w 2` exit 0
  after 2.0s both after input ended and
  with input held open but silent.
  The `-q` flag is quoted from the
  local man page, not separately timed.
- The resolver surprise: the build
  sandbox's resolver answers
  `no-such-host.invalid` with
  198.18.83.181 and a connect to it
  "succeeds" — captured whole, and
  taught in chapter 13 as an
  environment artefact, not netcat
  behaviour.

**Documented-only (not run), and why:**

- *Traditional netcat and ncat
  behaviour* (all of chapter 12's
  non-OpenBSD columns). Neither program
  is installed on the build machine,
  and the guide says so where it
  matters. Their flags were checked
  against the projects' own man pages
  during the build — that check caught
  one real error before publication:
  ncat has no `-N`; its spelling is
  `--send-only` — and the table says
  so. The OpenBSD column is captured;
  the other two are documentation,
  labelled as such.
- *The OpenBSD manual's `-c`/`-e`
  passage* quoted in chapter 11: the
  wording is the manual's, from the
  man page installed on the build
  machine. The fd-redirection
  execution it warns about was not
  performed.
- *Connecting to services beyond the
  lab* (real SSH/SMTP banners and the
  like): described in prose in
  chapters 2–3 from the protocols'
  public behaviour. Every target this
  guide actually connected to is the
  build machine itself, on loopback.
- *Non-loopback, cross-machine
  behaviour generally:* the sandbox's
  only other address is its fabric's,
  which is not the guide's to probe.
  Consequences the chapters flag
  rather than demonstrate: UDP checks
  over filtered networks (the shrug
  is argued from the loopback
  captures' contrast), the firewall
  recipe run from a second machine,
  and transfer timings. Nothing
  depends on an invented remote.
- *Windows and macOS netcat:* named
  (third-party `nc.exe` builds exist
  and vary in trustworthiness; macOS
  ships a close OpenBSD relative);
  no non-Linux machine was available
  to the build.

Specimen discipline, for the record:
every connection in this guide targets
127.0.0.1 or a Unix socket in the lab
directory, and every listener binds
127.0.0.1. The one iptables rule used
(DROP on the lab's own port) was added
for a single capture and removed
immediately after, with the removal
verified. No output was completed,
corrected, or invented: where a capture
surprised the draft — the backlog
caller's exit 0, `-z`'s asymmetric
reporting, the resolver that answers
anything — the chapters were written
to the capture.
