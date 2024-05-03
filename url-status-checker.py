import argparse
import httpx
import asyncio
from tqdm import tqdm
from colorama import Fore, Style

# Banner
BANNER = """
╔═══════════════════════════════╗
║       StatusChecker.py        ║
║   Created By: BLACK_SCORP10   ║
║   Telegram: @BLACK_SCORP10    ║
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

# Function to check URL status
async def check_url_status(session, url_id, url):
    if "://" not in url:
        url = "https://" + url  # Adding https:// if no protocol is specified
    try:
        response = await session.head(url)
        return url_id, url, response.status_code
    except httpx.RequestError:
        return url_id, url, None

# Function to parse arguments
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

    async with httpx.AsyncClient(follow_redirects=True) as session:
        results = {}
        tasks = [check_url_status(session, url_id, url) for url_id, url in enumerate(urls)]
        if len(urls) > 1:
            with tqdm(total=len(urls), desc="Checking URLs") as pbar:
                for coro in asyncio.as_completed(tasks):
                    url_id, url, status_code = await coro
                    results[url_id] = (url, status_code)
                    pbar.update(1)
        else:
            for coro in asyncio.as_completed(tasks):
                url_id, url, status_code = await coro
                results[url_id] = (url, status_code)

    status_codes = {
        "1xx": [],
        "2xx": [],
        "3xx": [],
        "4xx": [],
        "5xx": [],
        "Invalid": []
    }

    for url_id, (url, status) in results.items():
        if status is not None:
            status_group = str(status)[0] + "xx"
            status_codes[status_group].append((url, status))
        else:
            status_codes["Invalid"].append((url, "Invalid"))

    for code, urls in status_codes.items():
        if urls:
            print(COLORS.get(code, Fore.WHITE) + f'===== {code.upper()} =====')
            for url, status in urls:
                print(f'[Status : {status}] = {url}')
            print(Style.RESET_ALL)

    if args.output:
        with open(args.output, 'w') as file:
            for code, urls in status_codes.items():
                if urls:
                    file.write(f'===== {code.upper()} =====\n')
                    for url, status in urls:
                        file.write(f'[Status : {status}] = {url}\n')

if __name__ == "__main__":
    asyncio.run(main())
