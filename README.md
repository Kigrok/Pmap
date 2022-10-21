# Pmap

![Pmap Logo](https://lh3.googleusercontent.com/drive-viewer/AJc5JmTJMZHWfj51bhxa9Oib1P_uIcBEcsuycMmX-K-Kaxm3rLNehMjLX6ODkUaL0GCa3-TRkdIpEPw=w1366-h656)

## Multi-threaded port scanner


- Port check and information from it
- Selecting the number of threads
- MSelecting a range of ports to scan

![Pmap](https://lh3.googleusercontent.com/drive-viewer/AJc5JmTF3C5CTaiUixrIiLJjjltau2pAqpwu3rkdwoO_qKF1SDYA2jkcFQ0VXTDanNv00_Rq1cQQCKc=w1366-h612)

---

## Help

![Help](https://lh3.googleusercontent.com/drive-viewer/AJc5JmRRLhwSYd4TBjhiSjxI76pmX36-F8A4J7YxW5RQd0wqJp7MNOCJkMZh97DDXpKc42zOwMitE8o=w1366-h656)

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
python3 pmap.py  -u [ URL]  -p [ PORT] -t [ THREADS]
```
