import tkinter as tk
from tkinter import messagebox
import json
import os

filename = "userdatabase.json"
BG_COLOR = "#2C3E50"
BTN_COLOR = "#1ABC9C"
TEXT_COLOR = "#ECF0F1"
ENTRY_BG = "#34495E"
FONT = ("Helvetica", 12)

# Load data
def load_data():
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            return json.load(file)
    else:
        return []

# Save data
def save_data(data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

# Beautiful window wrapper
def create_window(title):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("400x400")
    win.config(bg=BG_COLOR)
    return win

# Entry label + field
def create_labeled_entry(parent, label_text, show=None):
    tk.Label(parent, text=label_text, font=FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=5)
    entry = tk.Entry(parent, font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, show=show)
    entry.pack(pady=5, ipadx=10, ipady=5)
    return entry

# Styled button
def create_button(parent, text, command):
    return tk.Button(parent, text=text, command=command, bg=BTN_COLOR, fg="white", font=FONT,
                     activebackground="#16A085", relief="flat", padx=10, pady=5)

# Sign Up Window
def signup_window():
    win = create_window("Sign Up")
    name_entry = create_labeled_entry(win, "Name:")
    email_entry = create_labeled_entry(win, "Email:")
    pass_entry = create_labeled_entry(win, "Password:", show="*")

    def submit():
        name, email, password = name_entry.get(), email_entry.get(), pass_entry.get()
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields required")
            return
        data = load_data()
        data.append({"name": name, "email": email, "pass": password})
        save_data(data)
        messagebox.showinfo("Success", f"Account Created for {name}")
        win.destroy()

    create_button(win, "Create Account", submit).pack(pady=20)

# Login Window
def login_window():
    win = create_window("Login")
    email_entry = create_labeled_entry(win, "Email:")
    pass_entry = create_labeled_entry(win, "Password:", show="*")

    def login():
        email, password = email_entry.get(), pass_entry.get()
        data = load_data()
        for user in data:
            if user["email"] == email and user["pass"] == password:
                messagebox.showinfo("Success", "Login Successful")
                win.destroy()
                return
        messagebox.showerror("Error", "Invalid credentials")

    create_button(win, "Login", login).pack(pady=20)

# Change Password Window
def change_password_window():
    win = create_window("Change Password")
    email_entry = create_labeled_entry(win, "Email:")
    old_entry = create_labeled_entry(win, "Old Password:", show="*")
    new_entry = create_labeled_entry(win, "New Password:", show="*")

    def change():
        email, old, new = email_entry.get(), old_entry.get(), new_entry.get()
        data = load_data()
        found = False
        for user in data:
            if user["email"] == email and user["pass"] == old:
                user["pass"] = new
                found = True
                break
        if found:
            save_data(data)
            messagebox.showinfo("Success", "Password Changed")
            win.destroy()
        else:
            messagebox.showerror("Error", "Incorrect email or old password")

    create_button(win, "Change Password", change).pack(pady=20)

# Delete Account Window
def delete_account_window():
    win = create_window("Delete Account")
    email_entry = create_labeled_entry(win, "Email:")
    pass_entry = create_labeled_entry(win, "Password:", show="*")

    def delete():
        email, password = email_entry.get(), pass_entry.get()
        data = load_data()
        new_data = [u for u in data if not (u["email"] == email and u["pass"] == password)]
        if len(new_data) != len(data):
            save_data(new_data)
            messagebox.showinfo("Success", "Account Deleted")
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    create_button(win, "Delete Account", delete).pack(pady=20)

# Main Menu
def main_menu():
    root = tk.Tk()
    root.title("User Auth System")
    root.geometry("450x500")
    root.config(bg=BG_COLOR)

    tk.Label(root, text="Json-Based User Auth System", font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)

    create_button(root, "Sign Up", signup_window).pack(pady=10, ipadx=20)
    create_button(root, "Login", login_window).pack(pady=10, ipadx=20)
    create_button(root, "Change Password", change_password_window).pack(pady=10, ipadx=20)
    create_button(root, "Delete Account", delete_account_window).pack(pady=10, ipadx=20)
    create_button(root, "Exit", root.destroy).pack(pady=30, ipadx=20)

    root.mainloop()

# Run the app
main_menu()

