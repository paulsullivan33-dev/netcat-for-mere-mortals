# HTTP by Hand

Here is the moment netcat exists for.
Serve the lab's specimen page with
Python's built-in web server:

```
$ cd examples
$ python3 -m http.server 45003 --bind 127.0.0.1
```

(its own terminal — it will log every
request there, which is half the fun).
Now, from another terminal, fetch the
page the way a browser does, except
that *you* are the browser:

```
$ printf "GET / HTTP/1.0\r\n\r\n" | nc -N -w 3 127.0.0.1 45003
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.3
Date: Tue, 20 Oct 2026 19:21:33 GMT
Content-type: text/html
Content-Length: 286
Last-Modified: Tue, 20 Oct 2026 19:20:55 GMT

<!DOCTYPE html>
<html>
<head><title>Lab Web - Specimen Page</title></head>
<body>
<h1>Specimen page</h1>
<p>This page exists so the netcat lab has something real
to fetch by hand. If you are reading this in a terminal,
you typed an HTTP request yourself. Well done.</p>
</body>
</html>
```

Your entire contribution to that
exchange was one line — `GET / HTTP/1.0`
— followed by a blank line (the
`\r\n\r\n` is two carriage-return +
line-feed pairs: the end of the request
line, then the empty line that says
"that's all"). Everything else in the
capture is the server:

- **The status line** — `HTTP/1.0 200 OK`:
  the protocol's version, the code, and
  the code's name in words. 200 is the
  famous one; you meet another below.
- **The headers** — one `Name: value`
  per line: what the server is
  (`Server:`), when it answered
  (`Date:`), what it's sending
  (`Content-type:`), and — the one
  netcat cares about most — exactly
  **how many bytes of body follow**
  (`Content-Length: 286`).
- **A blank line**, the mirror of yours:
  headers over.
- **The body** — 286 bytes of it, the
  specimen page itself.

That's an HTTP transaction with the
envelope removed. When the *curl* guide
shows you `-v` output with its `>` and
`<` lines, this is the conversation
it's annotating; you have now had it
without the annotation.

## Asking for something that isn't there

```
$ printf "GET /no-such-page HTTP/1.0\r\n\r\n" | nc -N -w 3 127.0.0.1 45003
HTTP/1.0 404 File not found
Server: SimpleHTTP/0.6 Python/3.12.3
Date: Tue, 20 Oct 2026 19:21:33 GMT
Connection: close
Content-Type: text/html;charset=utf-8
Content-Length: 335
...
```

Same shape, different story: the status
line carries the famous 404, and the
body is an apology in HTML. (The capture
is trimmed at the body here — the full
error page is in the lab transcripts.)
The lesson is worth the detour: an HTTP
"error" is not a failed conversation.
The socket worked perfectly; the
*protocol* said no. Netcat's exit code
agrees — this exchange also ends 0,
because netcat's job is the socket, and
the socket succeeded. Tools that care
about the 404 (curl's `--fail`, your
browser's sad face) care on top of the
socket, in the protocol layer netcat
deliberately doesn't have.

## Why bother, when curl exists?

Three mortal reasons:

- **The server is lying and you want
  the raw tape.** Redirects, browser
  content negotiation, and helpful
  libraries all edit the conversation.
  Netcat shows the bytes that actually
  crossed.
- **There's no curl there.** A minimal
  container, a broken appliance, a
  rescue shell: if it has `nc`, you can
  still ask the web service what it
  thinks.
- **The service isn't HTTP.** The same
  by-hand posture works on any
  text-shaped protocol: greet a mail
  server, type `EHLO me`, read the
  reply. The protocols differ; the
  handset doesn't.

One limit, plainly: **HTTPS will not
talk to you this way.** A TLS server
expects a cryptographic handshake, not
text — netcat will connect, and then
the two of you will sit in encrypted
silence. For the by-hand TLS
conversation, the tool is `openssl
s_client` and its own guide in this
series; `ncat --ssl` (chapter 12) is
the netcat-family answer, but it is not
the OpenBSD `nc` taught here.

Check: look at the web server's own
terminal after both fetches. It logged
both requests — `"GET / HTTP/1.0" 200`
and `"GET /no-such-page HTTP/1.0" 404` —
the server's side of the same two
conversations, kept whether the client
was you, netcat, or a browser.
