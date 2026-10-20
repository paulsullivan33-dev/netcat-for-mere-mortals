#!/usr/bin/env python3
"""Lab fixture for Netcat for Mere Mortals.

Stands up one small specimen service on 127.0.0.1:

  * a banner + echo server on tcp/45002. It greets every
    connection with one line, then sends back whatever it
    receives, line for line. It is not SSH, not HTTP, not
    anything with a phone-book entry -- it is a machine that
    says hello and repeats you, which is all a netcat lab
    needs.

Everything binds to the loopback address only. Nothing here
faces a network.

Usage:
    python3 lab_server.py            # serve until Ctrl-C
    python3 lab_server.py --check    # print the plan and exit
"""

import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = 45002
BANNER = b"LabEcho/1.0 -- a lab fixture: it says hello, then repeats you.\r\n"


def handle(conn, addr):
    try:
        conn.sendall(BANNER)
        buf = b""
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                conn.sendall(line + b"\n")
    except (ConnectionResetError, BrokenPipeError):
        # A client hung up rudely (netcat users do this
        # constantly). That's the client's business; the
        # fixture shrugs and keeps serving.
        pass
    finally:
        try:
            conn.close()
        except OSError:
            pass


def main():
    if "--check" in sys.argv:
        print(f"banner+echo fixture: tcp/{PORT} on {HOST}")
        print("banner:", BANNER.decode().strip())
        print("deliberately closed specimen: tcp/45999 (nothing binds it)")
        return
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(8)
    print(f"LabEcho listening on {HOST}:{PORT} -- Ctrl-C to stop", flush=True)
    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
