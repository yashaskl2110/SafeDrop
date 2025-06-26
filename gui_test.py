import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from collections import defaultdict
import time
import os
import platform
import shutil

from core.watcher import start_watching
from core.utils import sanitize

# Globals
leak_log = []
current_folder = None
watcher_thread = None
watching = False
current_page = 0
FILES_PER_PAGE = 10
leak_type_counts = defaultdict(int)
file_set = set()
dark_mode = False
report_visible = True

# Quarantine setup
quarantine_folder = os.path.join(os.getcwd(), "quarantine")
os.makedirs(quarantine_folder, exist_ok=True)

def quarantine_file(file_path):
    try:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            dest = os.path.join(quarantine_folder, filename)
            shutil.move(file_path, dest)
            print(f"[QUARANTINED] Moved to: {dest}")
    except Exception as e:
        print(f"[!] Failed to quarantine {file_path}: {e}")

def log_leak_gui(timestamp, file_path, label, value):
    first_time = file_path not in file_set
    sanitized_value = sanitize(value)
    leak_log.append((timestamp, file_path, label, sanitized_value))
    file_set.add(file_path)
    leak_type_counts[label] += 1
    update_table()
    update_summary()

    if first_time:
        play_alert()
        quarantine_file(file_path)
        messagebox.showwarning("Leak Detected!", f"Sensitive data found in:\n{file_path}\nFile has been quarantined.")

def play_alert():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep()
        else:
            print('\a')
    except:
        pass

def update_table():
    tree.delete(*tree.get_children())
    start = current_page * FILES_PER_PAGE
    end = start + FILES_PER_PAGE
    for entry in leak_log[start:end]:
        tree.insert('', 'end', values=entry)
    update_nav_buttons()

def update_summary():
    summary_table.delete(*summary_table.get_children())
    for label, count in leak_type_counts.items():
        summary_table.insert("", "end", values=(label, count))
    summary_label.config(text=f"📂 Files scanned: {len(file_set)}   🔐 Leaks detected: {len(leak_log)}")

def choose_folder():
    global current_folder
    selected = filedialog.askdirectory()
    if selected:
        current_folder = selected
        folder_label.config(text=f"Watching: {selected}")

def start_monitoring():
    global watcher_thread, watching
    if not current_folder:
        messagebox.showwarning("No Folder", "Please select a folder to watch.")
        return
    if watching:
        messagebox.showinfo("Already Watching", "Monitoring is already running.")
        return

    def threaded_watch():
        global watching
        watching = True
        start_watching(current_folder, log_callback=log_leak_gui)

    watcher_thread = threading.Thread(target=threaded_watch, daemon=True)
    watcher_thread.start()
    status_label.config(text="🟢 Monitoring Active")

def stop_monitoring():
    global watching
    watching = False
    status_label.config(text="🔴 Monitoring Stopped")
    messagebox.showinfo("Stopped", "Monitoring has been stopped manually.")

def next_page():
    global current_page
    if (current_page + 1) * FILES_PER_PAGE < len(leak_log):
        current_page += 1
        update_table()

def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        update_table()

def update_nav_buttons():
    prev_btn.config(state="normal" if current_page > 0 else "disabled")
    next_btn.config(state="normal" if (current_page + 1) * FILES_PER_PAGE < len(leak_log) else "disabled")

def open_quarantine_folder():
    try:
        if platform.system() == "Windows":
            os.startfile(quarantine_folder)
        elif platform.system() == "Darwin":
            os.system(f"open {quarantine_folder}")
        else:
            os.system(f"xdg-open {quarantine_folder}")
    except Exception as e:
        print(f"[!] Failed to open quarantine folder: {e}")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2e2e2e" if dark_mode else "#f0f0f0"
    fg = "#ffffff" if dark_mode else "#000000"
    root.config(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass

def toggle_report_panel():
    global report_visible
    if report_visible:
        report_frame.pack_forget()
        report_toggle_btn.config(text="Show Analysis Report")
    else:
        report_frame.pack(fill="x", padx=10, pady=5)
        report_toggle_btn.config(text="Hide Analysis Report")
    report_visible = not report_visible

# GUI setup
root = tk.Tk()
root.title("SafeDrop Leak Monitor")
root.geometry("980x700")
root.minsize(800, 600)

# Top controls
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="Select Folder", command=choose_folder).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Start", bg="green", fg="white", command=start_monitoring).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Stop", bg="red", fg="white", command=stop_monitoring).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="🌓 Toggle Theme", command=toggle_dark_mode).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Open Quarantine Folder", command=open_quarantine_folder).pack(side=tk.LEFT, padx=5)

# Status and folder info
folder_label = tk.Label(root, text="No folder selected", fg="blue")
folder_label.pack()
status_label = tk.Label(root, text="🔴 Monitoring Stopped", fg="red")
status_label.pack()

# Leak table
tree_frame = tk.Frame(root)
tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

columns = ("Timestamp", "File Path", "Leak Type", "Leak Value")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
tree.pack(expand=True, fill="both")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Leak Value" else 300)

# Navigation
nav_frame = tk.Frame(root)
nav_frame.pack()
prev_btn = tk.Button(nav_frame, text="⏮ Prev", command=prev_page)
prev_btn.pack(side=tk.LEFT, padx=5)
next_btn = tk.Button(nav_frame, text="Next ⏭", command=next_page)
next_btn.pack(side=tk.LEFT, padx=5)

# Summary toggle and panel
report_toggle_btn = tk.Button(root, text="Hide Analysis Report", command=toggle_report_panel)
report_toggle_btn.pack(pady=5)

report_frame = tk.Frame(root)
report_frame.pack(fill="x", padx=10, pady=5)

summary_label = tk.Label(report_frame, text="📂 Files scanned: 0   🔐 Leaks detected: 0", font=("Arial", 10, "bold"))
summary_label.pack(anchor="w")

summary_table = ttk.Treeview(report_frame, columns=("Leak Type", "Count"), show="headings", height=5)
summary_table.heading("Leak Type", text="Leak Type")
summary_table.heading("Count", text="Count")
summary_table.column("Leak Type", width=200)
summary_table.column("Count", width=100)
summary_table.pack(fill="x", padx=5, pady=2)

# Init
update_table()
root.mainloop()
