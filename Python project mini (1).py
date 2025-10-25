import tkinter as tk
from tkinter import ttk, messagebox
import re
import random
import string
from datetime import datetime

# ----------------- Password Strength Function -----------------
def check_strength(event=None):
    password = entry.get()
    strength = 0

    if len(password) >= 6:
        strength += 1
    if len(password) >= 10:
        strength += 1
    if re.search("[a-z]", password):
        strength += 1
    if re.search("[A-Z]", password):
        strength += 1
    if re.search("[0-9]", password):
        strength += 1
    if re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1

    progress["value"] = (strength / 6) * 100

    if strength <= 2:
        result_label.config(text="Weak 🔴", fg=current_colors["weak"])
    elif strength <= 4:
        result_label.config(text="Medium 🟡", fg=current_colors["medium"])
    else:
        result_label.config(text="Strong 🟢", fg=current_colors["strong"])

# ----------------- Suggest Strong Password -----------------
def suggest_password():
    lower = random.choices(string.ascii_lowercase, k=4)
    upper = random.choices(string.ascii_uppercase, k=3)
    digits = random.choices(string.digits, k=3)
    symbols = random.choices("!@#$%^&*()_+-=[]{}|;:,.<>?", k=3)
    all_chars = lower + upper + digits + symbols
    random.shuffle(all_chars)
    strong_pass = ''.join(all_chars)
    entry.delete(0, tk.END)
    entry.insert(0, strong_pass)
    check_strength()
    messagebox.showinfo("Suggested Password", f"Here's a strong password suggestion:\n\n{strong_pass}")

# ----------------- Toggle Password Visibility -----------------
def toggle_password():
    if entry.cget("show") == "":
        entry.config(show="*")
        eye_button.config(text="👁")
    else:
        entry.config(show="")
        eye_button.config(text="🙈")

# ----------------- Copy Password -----------------
def copy_password():
    password = entry.get()
    if password.strip() == "":
        messagebox.showwarning("Empty", "No password to copy!")
        return
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# ----------------- Live Clock -----------------
def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")
    clock_label.config(text=now)
    clock_label.after(1000, update_clock)

# ----------------- Color Theme -----------------
current_colors = {
    "bg": "#0b0f0b",
    "panel": "#101c10",
    "accent": "#00ff88",
    "text": "#7CFC00",
    "entry_bg": "#0f2410",
    "entry_fg": "#00ff88",
    "trough": "#1a2a1a",
    "weak": "#ff4d4d",
    "medium": "#ffc107",
    "strong": "#00ff88"
}

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Pass Checker")
root.state("zoomed")
root.configure(bg=current_colors["bg"])

main_frame = tk.Frame(root, bg=current_colors["panel"], bd=3, relief="ridge")
main_frame.pack(expand=True, fill="both", padx=100, pady=100)

title_label = tk.Label(main_frame, text="💀 Pass Checker",
                       bg=current_colors["panel"], font=("Consolas", 26, "bold"),
                       fg=current_colors["accent"])
title_label.pack(pady=(10, 20))

clock_label = tk.Label(main_frame, text="", bg=current_colors["panel"],
                       font=("Consolas", 14), fg=current_colors["text"])
clock_label.pack(pady=(0, 30))
update_clock()

entry_frame = tk.Frame(main_frame, bg=current_colors["panel"])
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, show="*", width=35, font=("Consolas", 18),
                 bd=2, relief="groove", justify="center",
                 bg=current_colors["entry_bg"], fg=current_colors["entry_fg"],
                 insertbackground=current_colors["accent"])
entry.grid(row=0, column=0, padx=(0, 10))
entry.bind("<KeyRelease>", check_strength)

eye_button = tk.Button(entry_frame, text="👁", bg=current_colors["panel"],
                       fg=current_colors["accent"], bd=0,
                       font=("Consolas", 14), command=toggle_password,
                       cursor="hand2")
eye_button.grid(row=0, column=1)

style = ttk.Style()
style.theme_use("default")
style.configure("TProgressbar", thickness=20, troughcolor=current_colors["trough"],
                background=current_colors["accent"], bordercolor=current_colors["panel"],
                lightcolor=current_colors["accent"], darkcolor=current_colors["accent"])

progress = ttk.Progressbar(main_frame, length=500, mode="determinate", style="TProgressbar")
progress.pack(pady=25)

result_label = tk.Label(main_frame, text="Type a password to begin...",
                        font=("Consolas", 16), bg=current_colors["panel"], fg=current_colors["text"])
result_label.pack(pady=10)

# ----------------- Buttons -----------------
button_frame = tk.Frame(main_frame, bg=current_colors["panel"])
button_frame.pack(pady=20)

suggest_button = tk.Button(button_frame, text="💡 Suggest Strong Password",
                           font=("Consolas", 13, "bold"),
                           bg=current_colors["panel"], fg=current_colors["accent"],
                           bd=1, cursor="hand2", command=suggest_password)
suggest_button.grid(row=0, column=0, padx=10)

copy_button = tk.Button(button_frame, text="📋 Copy Password",
                        font=("Consolas", 13, "bold"),
                        bg=current_colors["panel"], fg=current_colors["accent"],
                        bd=1, cursor="hand2", command=copy_password)
copy_button.grid(row=0, column=1, padx=10)

root.mainloop()
