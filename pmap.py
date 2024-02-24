#!/usr/bin/env python3

from socket import gethostbyname, socket, AF_INET, SOCK_STREAM
from argparse import ArgumentParser, Namespace
from aiohttp import ClientSession
from multiprocessing import Pool
from datetime import datetime
from pyfiglet import Figlet
from asyncio import run
import json

def get_args() -> Namespace:
    """
    Retrieve command-line arguments.
    Returns:
        argparse.Namespace: A namespace containing command-line arguments.
    """
    parser: ArgumentParser = ArgumentParser(description='Pmap ~ Async Port Scanner')
    parser.add_argument('url', type=str, help='URL of the website to scan')
    parser.add_argument('-p', '--ports', type=int, default=65535, help='Number of ports to scan (default: 65535)')
    parser.add_argument('-t', '--threads', type=int, default=500, help='Number of threads for scanning (default: 500)')
    return parser.parse_args()

async def fetch_url(url: str) -> ClientSession:
    """
    Fetches the content of a URL asynchronously.
    Args:
        url (str): The URL to fetch.
    Returns:
        aiohttp.ClientResponse: The response object containing the fetched content.
    """
    async with ClientSession() as session:
        async with session.get(str(url)) as response:
            return response

async def geo_info(ip: str) -> str | Exception:
    """
    Retrieves geographical information for a given IP address using an external API.
    Args:
        ip (str): The IP address for which to retrieve information.
    Returns:
        str: A formatted string containing the geographical information.
        Exception: An exception raised if the retrieval process fails.
    """
    try:
        async with ClientSession() as session:
            async with session.get(f'http://ip-api.com/json/{ip}') as response:
                data: json = await response.json()
                return f'''Country: \033[34m{data['country']} | {data['countryCode']}\033[00m\n\
Sity: \033[34m{data['city']}\033[00m\n\
TimeZone: \033[34m{data['timezone']}\033[00m'''
    except Exception as e: 
        raise e

async def success(response: ClientSession, ip: str) -> str:
    """
    Formats and constructs a success message containing information about the response and IP address.
    Args:
        response (ClientSession): The response object from the website.
        ip (str): The IP address of the website.
    Returns:
        str: A formatted success message containing details about the response, IP address, server, and timestamp.
    """
    return(f'''{'-'*40}\n{response.host} | \033[36m{ip}\033[00m (\033[32m{response.status}\033[00m)
Star Scan: \033[36m{(datetime.now()).strftime("%d-%m-%Y %H:%M:%S")}\033[00m
Server: \033[36m{response.headers.get("Server")}\033[00m
X-Powered-By: \033[36m{response.headers.get("X-Powered-By")}\033[00m
{'*'*30}\n{str(await geo_info(ip=str(ip)))}\n{'-'*40}''')

async def get_website_info(url: str, ports: int, threads: int) -> None | Exception:
    """
    Retrieves information about a website, such as its IP address, and initiates port scanning.
    Args:
        url (str): The URL of the website to scan.
        ports (int): The number of ports to scan.
        threads (int): The number of threads for scanning.
    Raises:
        Exception: If an error occurs during the process.
    """
    try:
        response: ClientSession = await fetch_url(url=str(url))
        ip: str = gethostbyname(response.host)
        print(await success(response=response, ip=str(ip)))
        await proccessing(ip=str(ip), ports=list(range(ports)), threads=int(threads))
    except Exception as e:
        raise e

async def proccessing(ip: str, ports: list[int], threads: int) -> None:
    """
    Initiates port scanning for the specified IP address and ports using multiprocessing.
    Args:
        ip (str): The IP address to scan.
        ports (list[int]): A list of port numbers to scan.
        threads (int): The number of threads for scanning.
    Raises:
        OSError: If an error occurs during multiprocessing.
    """
    try:
        with Pool(processes=int(threads)) as process:
            process.starmap(scan_port, [(ip, port) for port in ports])
    except OSError as e:
        print(f'\033[31m{e}\033[00m') 

def port_info(port: int, data: bytes) -> str:
    """
    Analyzes the received data and generates a string representing port information.
    Args:
        port (int): The port number.
        data (bytes): The data received from the port.
    Returns:
        str: A formatted string containing port information.
    """
    data: bytes = data.strip().decode('utf-8')
    if 'html' in (data).lower():
        data: str = '<HTML>'
    return(f'''[\033[31m+\033[00m] Port: \033[95m{port}\033[00m ~ \033[93m{data}\033[00m''')

def scan_port(ip: str, port: int) -> None:
    """
    Scans a specific port on the given IP address and prints the port information.
    Args:
        ip (str): The IP address to scan.
        port (int): The port number to scan.
    """
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\n\r\n')
            try:
                print(port_info(port=int(port), data=bytes(sock.recv(8192))))
            except: 
                print(port_info(port=int(port), data=bytes(sock.recv(4096))))
        except: pass

async def main():
    """
    Main entry point of the program. It prints the ASCII art title of the program,
    gets command-line arguments using get_args function, and then calls the get_website_info
    function with the provided URL, ports, and threads.
    """
    print(f'\033[31m{Figlet(font="slant").renderText("Pmap")}\033[00m')
    await get_website_info(url=str(get_args().url), ports=int(get_args().ports), threads=int(get_args().threads))

if __name__ == "__main__":
    run(main())