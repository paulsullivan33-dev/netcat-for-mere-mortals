# The Double Edge

Every other chapter has been politely
not saying something. Here it is:
**the commands in this guide are, byte
for byte, the commands of the classic
network backdoor.** A listening netcat
that runs commands for whoever connects
was the first "remote access tool" a
generation of intruders reached for,
and "is netcat installed?" is still a
real question in incident response.
The tool is not two tools. Judging it
means looking at the shape, not the
binary — so let's look.

## The shape that makes it a backdoor

Three properties, all of which you've
used legitimately by now:

- **It listens without authenticating.**
  Whoever connects is the peer
  (chapter 6's "whoever connects
  first" warning).
- **It moves arbitrary bytes** —
  files in, files (and command output)
  out.
- **It can be wired to a shell.**
  Chapter 7 showed `nc ... | sh` and
  labelled it. The OpenBSD netcat
  removes the traditional `-e` flag
  that ran a program on connect — its
  own manual says so, in words worth
  quoting:

  > There is no -c or -e option in this
  > netcat, but you still can execute a
  > command after connection being
  > established by redirecting file
  > descriptors. Be cautious here
  > because opening a port and let
  > anyone connected execute arbitrary
  > command...

  The designers removed the button and
  kept the machinery, because the
  machinery *is* the tool. The caution
  is the user's part of the design.

## The same shape, on the admin's side

Why mortals keep it anyway — the uses
this guide actually teaches:

- **The one-file rescue.** A machine
  with a broken package manager, a
  minimal container, a rescue shell:
  `scp` needs a working sshd and auth;
  netcat needs one command at each end
  and the file is across (chapter 6),
  hashes checked, listener gone.
- **The "is it alive behind the
  firewall" verdict** (chapter 5) —
  settling, in ten seconds, an argument
  between a service team and a network
  team that email would take a day to
  lose.
- **The by-hand protocol conversation**
  (chapters 2–3): debugging a service
  by being its client, with no library
  editing the tape.
- **The report pipe** (chapter 7):
  moving a file or a command's output
  inside infrastructure you administer,
  one-shot, leaving nothing running.

Notice what the legitimate uses share
and the backdoor lacks: **they are
brief, bound to addresses the admin
controls, and started by the machine's
owner for a named purpose.** The
difference between a backdoor and a
pocketknife is not the edge — it's the
hand, the duration, and the door it's
on.

## The habits that keep it on the right side

1. **Bind loopback in every experiment**
   — `nc -l 127.0.0.1 ...`, as every
   lab in this guide does. A listener
   with no address binds *all*
   interfaces; that one omission is the
   whole difference between a lab and
   an exposure.
2. **One-shot over standing.** Take
   the listener down when the job is
   done; prefer the scheduled one-shot
   pattern of chapter 7 to a `-k` ear
   that outlives its purpose. A
   listener you forgot is a door you
   don't know about.
3. **Never wire a listener to a shell
   on anything reachable.** Not "just
   for a minute," not "only from the
   LAN." The minute is when it's found,
   and the LAN is an assumption, not a
   wall.
4. **Treat a found netcat listener
   like a found open door.** If you
   meet `nc -l` running on a machine
   and nobody can say why, that's an
   incident, not a curiosity — exactly
   as you'd treat an sshd you didn't
   install.

Check: audit yourself the way chapter
5 taught — from another of your
machines, `nc -zv` your workstation's
address on the lab ports after a
session. Nothing should answer. The
lab bound loopback, the listeners
exited, and the audit proves both —
which is the state this chapter is
trying to make into your default.
