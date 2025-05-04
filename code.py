import tkinter as tk
from tkinter import messagebox
import json
import os

filename = "userdatabase.json"

# Load data from file or return empty list
def load_data():
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            return json.load(file)
    return []

# Save data to file
def save_data(data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

# Sign Up Page
def signup_window():
    win = tk.Toplevel()
    win.title("Sign Up")
    win.geometry("300x300")

    tk.Label(win, text="Name:").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Email:").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Password:").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def submit():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = pass_entry.get().strip()
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        data = load_data()
        data.append({"name": name, "email": email, "pass": password})
        save_data(data)
        messagebox.showinfo("Success", f"Account created for {name}")
        win.destroy()

    tk.Button(win, text="Create Account", command=submit).pack(pady=10)

# Login Page
def login_window():
    win = tk.Toplevel()
    win.title("Login")
    win.geometry("300x200")

    tk.Label(win, text="Email:").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Password:").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def login():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()
        data = load_data()
        for user in data:
            if user["email"] == email and user["pass"] == password:
                messagebox.showinfo("Success", "Login Successful")
                win.destroy()
                return
        messagebox.showerror("Error", "Invalid credentials")

    tk.Button(win, text="Login", command=login).pack(pady=10)

# Change Password Page
def change_password_window():
    win = tk.Toplevel()
    win.title("Change Password")
    win.geometry("300x250")

    tk.Label(win, text="Email:").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Old Password:").pack()
    old_entry = tk.Entry(win, show="*")
    old_entry.pack()

    tk.Label(win, text="New Password:").pack()
    new_entry = tk.Entry(win, show="*")
    new_entry.pack()

    def change():
        email = email_entry.get().strip()
        old = old_entry.get().strip()
        new = new_entry.get().strip()
        data = load_data()
        found = False
        for user in data:
            if user["email"] == email and user["pass"] == old:
                user["pass"] = new
                found = True
                break
        if found:
            save_data(data)
            messagebox.showinfo("Success", "Password changed")
            win.destroy()
        else:
            messagebox.showerror("Error", "Incorrect email or old password")

    tk.Button(win, text="Change Password", command=change).pack(pady=10)

# Delete Account Page
def delete_account_window():
    win = tk.Toplevel()
    win.title("Delete Account")
    win.geometry("300x200")

    tk.Label(win, text="Email:").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Password:").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def delete():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()
        data = load_data()
        new_data = [user for user in data if not (user["email"] == email and user["pass"] == password)]
        if len(new_data) != len(data):
            save_data(new_data)
            messagebox.showinfo("Success", "Account deleted")
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(win, text="Delete Account", command=delete).pack(pady=10)

# Main Window
def main_menu():
    root = tk.Tk()
    root.title("Json based User Auth System")
    root.geometry("300x300")

    tk.Label(root, text="User Authentication System", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Sign Up", width=25, command=signup_window).pack(pady=5)
    tk.Button(root, text="Login", width=25, command=login_window).pack(pady=5)
    tk.Button(root, text="Change Password", width=25, command=change_password_window).pack(pady=5)
    tk.Button(root, text="Delete Account", width=25, command=delete_account_window).pack(pady=5)
    tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

# Start the app
if __name__ == "__main__":
    main_menu()
