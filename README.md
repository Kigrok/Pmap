# Pmap
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?&logo=python&logoColor=python)](https://www.python.org) [![aiohttp](https://img.shields.io/static/v1?label=aiohttp&message=v3.9.3&logo=Aiohttp&colorColor=Aiohttp)](https://docs.aiohttp.org/en/stable/) [![License](https://img.shields.io/badge/License-MIT-black.svg)]() 
![Pmap Logo](https://lh3.googleusercontent.com/u/0/drive-viewer/AEYmBYSxgjU5_MP9MnYgzjNBQU6dekdoSuOAkES4jJ0Jh1iNNRjrkMZxojy0XibLAlggVpyMc0CQGeaxLp_wIlurqRINf6Vm=w1366-h659)
Pmap is a port scanner that allows a user to check for open ports on a specified website. Using asynchronous and multiprocessing approaches, the program scans the specified website for available ports and returns information about the status and contents of each open port. It also provides additional details about the server, including country, city, and time zone, using the IP address geolocation API.
---
## Multi-threaded port scanner

- Port scanning and port information
- Selecting the number of threads
- Select the range of ports to scan
- Getting information about an open port

---
## Install 
Cloning a repository
```sh
git clone https://github.com/Kigrok/Pmap.git
cd Pmap
```
Installing the virtual environment and packages
```sh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```
---
## Start
```sh
python3 pmap.py [-h] [-p PORTS] [-t THREADS] url
```
---
## Help
```
positional arguments:
  url                   URL of the website to scan

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Number of ports to scan (default: 65535)
  -t THREADS, --threads THREADS
                        Number of threads for scanning (default: 500)

```
---
## License
[MIT](LICENSE) Copyright 2023 Venera, Inc.
