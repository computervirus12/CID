import os
import subprocess
import time
import datetime
import random
import ctypes
import platform
import webbrowser
from datetime import date

# Standard Windows API for battery (No external pip install needed)
class PowerStatus(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', ctypes.c_byte),
        ('BatteryFlag', ctypes.c_byte),
        ('BatteryLifePercent', ctypes.c_byte),
        ('Reserved1', ctypes.c_byte),
        ('BatteryLifeTime', ctypes.c_ulong),
        ('BatteryFullLifeTime', ctypes.c_ulong),
    ]

class CID_Ultimate:
    def __init__(self):
        os.system('') # Enable ANSI Colors
        self.log_file = "cid_final_history.log"
        self.prompt_color = '\033[96m' # Cyan
        self.is_cid_mode = True

    def get_battery(self):
        status = PowerStatus()
        if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            percent = status.BatteryLifePercent
            plugged = "Plugged In" if status.ACLineStatus == 1 else "On Battery"
            return f"{percent}% ({plugged})"
        return "Unknown"

    def about_pc(self):
        """Deep dive into PC specs using native Windows calls"""
        print(f"\n\033[92m--- CID SYSTEM DIAGNOSTICS ---")
        print(f"OS Platform:  {platform.system()} {platform.release()}")
        print(f"OS Version:   {platform.version()}")
        print(f"PC Name:      {platform.node()}")
        print(f"Processor:    {platform.processor()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Current Time: {time.strftime('%H:%M:%S')}")
        print(f"Current Date: {date.today()}")
        print(f"Battery:      {self.get_battery()}")
        print(f"------------------------------\033[0m\n")

    def web_search(self, query):
        print(f"Searching the web for: {query}...")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def run_glitch(self):
        print('\033[93m')
        try:
            for _ in range(100):
                line = "".join(random.choice("0123456789ABCDEF!@#$%^&*") for _ in range(80))
                print(line)
                time.sleep(0.03)
        except KeyboardInterrupt: pass
        print('\033[0m')

    def trap_mouse(self):
        print("\033[91m[MOUSE LOCKED] Press Ctrl+C to unlock!\033[0m")
        mid_x = ctypes.windll.user32.GetSystemMetrics(0) // 2
        mid_y = ctypes.windll.user32.GetSystemMetrics(1) // 2
        try:
            while True:
                ctypes.windll.user32.SetCursorPos(mid_x, mid_y)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\n\033[92m[MOUSE UNLOCKED]\033[0m")

    def run(self):
        os.system('cls')
        print(f"\033[96m\033[1mCID ULTIMATE v2.0 - FINAL BUILD\033[0m")
        print("Type 'about' for PC info or 'help' for commands.\n")

        while True:
            cwd = os.getcwd()
            mode = "CID" if self.is_cid_mode else "CMD"
            try:
                user_input = input(f"({mode}) {self.prompt_color}{cwd}> \033[0m").strip()
                if not user_input: continue

                # Logging
                with open(self.log_file, "a") as f:
                    f.write(f"[{datetime.datetime.now()}] {user_input}\n")

                parts = user_input.split()
                cmd = parts[0].lower()

                # --- Core Logic ---
                if cmd == "cmd": self.is_cid_mode = False
                elif cmd == "cid": self.is_cid_mode = True
                
                elif self.is_cid_mode:
                    if cmd == "about":
                        self.about_pc()
                    elif cmd == "time":
                        print(f"Current Time: {time.strftime('%I:%M %p')}")
                    elif cmd == "date":
                        print(f"Today's Date: {date.today().strftime('%B %d, %Y')}")
                    elif cmd == "battery":
                        print(f"Battery Status: {self.get_battery()}")
                    elif cmd == "search":
                        self.web_search(" ".join(parts[1:]))
                    elif cmd == "glitch":
                        self.run_glitch()
                    elif cmd == "mousetrap":
                        self.trap_mouse()
                    elif cmd == "make":
                        name = parts[1] if len(parts) > 1 else "note.txt"
                        with open(name, "w") as f: f.write("Created via CID.")
                        os.startfile(name)
                    elif cmd == "shutdown":
                        os.system("shutdown /s /t 10")
                    elif cmd == "help":
                        print("\nCID ULTIMATE COMMANDS:")
                        print("  about    - Detailed PC Specs & OS info")
                        print("  time     - Show current time")
                        print("  date     - Show current date")
                        print("  battery  - Check laptop battery %")
                        print("  search   - Search Google (e.g., search python tips)")
                        print("  glitch   - Jumbo matrix effect")
                        print("  mousetrap- Lock mouse (Ctrl+C to stop)")
                        print("  make [f] - Create & open a text file")
                        print("  cmd/cid  - Switch modes")
                        print("  exit     - Close project")
                    elif cmd == "exit": break
                    else: os.system(user_input)
                
                else: # Standard CMD Mode
                    if cmd == "exit": break
                    os.system(user_input)

            except KeyboardInterrupt: print("\nUse 'exit' to quit.")
            except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    CID_Ultimate().run()