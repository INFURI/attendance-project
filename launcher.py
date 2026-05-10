import tkinter as tk
import subprocess
import os

root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

def run_script(script):
    subprocess.run(["python", script])

def start_system():
    run_script("final_attendance.py")

def register_user():
    run_script("capture_faces.py")

def train_model():
    run_script("train_faces.py")

def view_attendance():
    os.startfile("attendance.xlsx")  


tk.Label(root, text="Smart Attendance System",
         font=("Arial", 16), bg="#1e1e1e", fg="white").pack(pady=20)

tk.Button(root, text="Start Attendance",
          width=25, command=start_system).pack(pady=5)

tk.Button(root, text="Register User",
          width=25, command=register_user).pack(pady=5)

tk.Button(root, text="Train Model",
          width=25, command=train_model).pack(pady=5)

tk.Button(root, text="View Attendance",
          width=25, command=view_attendance).pack(pady=5)

tk.Button(root, text="Exit",
          width=25, command=root.destroy).pack(pady=10)

root.mainloop()
