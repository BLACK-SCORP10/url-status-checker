import argparse
import httpx
import asyncio
from tqdm import tqdm
from colorama import Fore, Style
import socket
from urllib.parse import urlparse

# Banner
BANNER = """
╔═══════════════════════════════╗
║       StatusChecker.py        ║
║   Created By: BLACK_SCORP10   ║
║   Enanched By: matteocapricci ║
╚═══════════════════════════════╝
"""

# Color Codes
COLORS = {
    "1xx": Fore.WHITE,
    "2xx": Fore.GREEN,
    "3xx": Fore.YELLOW,
    "4xx": Fore.RED,
    "5xx": Fore.LIGHTRED_EX,
    "Invalid": Fore.WHITE
}

# Function to resolve hostname to IP:Port
def resolve_ip_and_port(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        scheme = parsed.scheme
        port = parsed.port or (443 if scheme == "https" else 80)
        ip_address = socket.gethostbyname(hostname)
        return f"{ip_address}:{port}"
    except Exception:
        return "IP:Port Not Found"

# Function to check URL status and redirection
async def check_url_status(session, url_id, url):
    if "://" not in url:
        url = "https://" + url
    try:
        response = await session.get(url, follow_redirects=True, timeout=10)
        final_url = str(response.url)

        original_ip_port = resolve_ip_and_port(url)
        redirect_ip_port = resolve_ip_and_port(final_url) if final_url != url else None

        return url_id, url, response.status_code, final_url if final_url != url else None, original_ip_port, redirect_ip_port
    except httpx.RequestError:
        return url_id, url, None, None, None, None

# Argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="URL Status Checker")
    parser.add_argument("-d", "--domain", help="Single domain/URL to check")
    parser.add_argument("-l", "--list", help="File containing list of domains/URLs to check")
    parser.add_argument("-o", "--output", help="File to save the output")
    parser.add_argument("-v", "--version", action="store_true", help="Display version information")
    parser.add_argument("-update", action="store_true", help="Update the tool")
    return parser.parse_args()

# Main function
async def main():
    args = parse_arguments()
    
    if args.version:
        print("StatusChecker.py version 1.0")
        return

    if args.update:
        print("Checking for updates...")  # Implement update logic here
        return

    print(BANNER)

    urls = set()

    if args.domain:
        urls.add(args.domain)
    elif args.list:
        with open(args.list, 'r') as file:
            urls.update(file.read().splitlines())
    else:
        print("No input provided. Use -d or -l option.")
        return

    async with httpx.AsyncClient() as session:
        results = {}
        tasks = [check_url_status(session, url_id, url) for url_id, url in enumerate(urls)]
        if len(urls) > 1:
            with tqdm(total=len(urls), desc="Checking URLs") as pbar:
                for coro in asyncio.as_completed(tasks):
                    url_id, url, status, redirect, ip, redirect_ip = await coro
                    results[url_id] = (url, status, redirect, ip, redirect_ip)
                    pbar.update(1)
        else:
            for coro in asyncio.as_completed(tasks):
                url_id, url, status, redirect, ip, redirect_ip = await coro
                results[url_id] = (url, status, redirect, ip, redirect_ip)

    status_codes = {
        "1xx": [],
        "2xx": [],
        "3xx": [],
        "4xx": [],
        "5xx": [],
        "Invalid": []
    }

    for url_id, (url, status, redirect, ip, redirect_ip) in results.items():
        if status is not None:
            status_group = str(status)[0] + "xx"
            status_codes[status_group].append((url, status, redirect, ip, redirect_ip))
        else:
            status_codes["Invalid"].append((url, "Invalid", None, "IP:Port Not Found", None))

    for code, urls_info in status_codes.items():
        if urls_info:
            print(COLORS.get(code, Fore.WHITE) + f'===== {code.upper()} =====')
            for url, status, redirect, ip, redirect_ip in urls_info:
                redirect_str = f"[Redirect: {redirect} ({redirect_ip})]" if redirect else "[Redirect: None]"
                print(f'[Status: {status}] [IP: {ip}] {url} {redirect_str}\n')
            print(Style.RESET_ALL)

    if args.output:
        with open(args.output, 'w') as file:
            for code, urls_info in status_codes.items():
                if urls_info:
                    file.write(f'===== {code.upper()} =====\n')
                    for url, status, redirect, ip, redirect_ip in urls_info:
                        redirect_str = f"[Redirect: {redirect} ({redirect_ip})]" if redirect else "[Redirect: None]"
                        file.write(f'[Status: {status}] [IP: {ip}] {url} {redirect_str}\n')

if __name__ == "__main__":
    asyncio.run(main())
