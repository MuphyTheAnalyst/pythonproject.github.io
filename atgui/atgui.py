#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import json

# Load user data from a JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to a JSON file
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Authenticate the user based on the data loaded from the JSON file
def authenticate_user(username, pin, users):
    user = users.get(username)
    if user and user["pin"] == pin:
        return user
    return None

# Add a new user to the JSON file
def add_user(username, pin, users):
    if username in users:
        return False  # User already exists
    users[username] = {
        "pin": pin,
        "balance": 0.0
    }
    save_users(users)
    return True

def login():
    username = username_entry.get()
    pin = pin_entry.get()
    user = authenticate_user(username, pin, users)
    if user:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or PIN")

def main_menu():
    main_window.withdraw()  # Hide the login window
    main_menu_window = tk.Toplevel(main_window)
    main_menu_window.title("ATM Options")

    def check_balance():
        messagebox.showinfo("Account Balance", f"Account Balance: ${user['balance']:.2f}")

    def withdraw():
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Invalid amount.")
        elif amount <= user['balance']:
            user['balance'] -= amount
            save_users(users)
            messagebox.showinfo("Withdrawal", f"Withdrew ${amount:.2f}. New balance: ${user['balance']:.2f}")
        else:
            messagebox.showerror("Insufficient Funds", "Insufficient funds.")

    def deposit():
        amount = float(amount_entry.get())
        if amount > 0:
            user['balance'] += amount
            save_users(users)
            messagebox.showinfo("Deposit", f"Deposited ${amount:.2f}. New balance: ${user['balance']:.2f}")
        else:
            messagebox.showerror("Invalid Amount", "Invalid amount.")

    def change_pin():
        new_pin = new_pin_entry.get()
        if len(new_pin) == 4:
            user['pin'] = new_pin
            save_users(users)
            messagebox.showinfo("Change PIN", "PIN changed successfully.")
        else:
            messagebox.showerror("Invalid PIN", "Invalid PIN format (4 characters required).")

    def add_new_user():
        new_username = new_username_entry.get()
        new_pin = new_pin_entry.get()
        if len(new_pin) == 4:
            if add_user(new_username, new_pin, users):
                messagebox.showinfo("User Added", "User added successfully.")
            else:
                messagebox.showerror("Username Exists", "Username already exists.")
        else:
            messagebox.showerror("Invalid PIN", "Invalid PIN format (4 characters required).")

    def exit():
        main_menu_window.destroy()
        main_window.deiconify()

    # Main menu buttons and widgets
    check_balance_button = tk.Button(main_menu_window, text="Check Balance", command=check_balance)
    withdraw_button = tk.Button(main_menu_window, text="Withdraw", command=withdraw)
    deposit_button = tk.Button(main_menu_window, text="Deposit", command=deposit)
    change_pin_button = tk.Button(main_menu_window, text="Change PIN", command=change_pin)
    add_new_user_button = tk.Button(main_menu_window, text="Add New User", command=add_new_user)
    exit_button = tk.Button(main_menu_window, text="Exit", command=exit)

    # Main menu widgets placement
    check_balance_button.pack()
    withdraw_button.pack()
    deposit_button.pack()
    change_pin_button.pack()
    add_new_user_button.pack()
    exit_button.pack()

    main_menu_window.mainloop()

def exit():
    main_window.destroy()

# Main window (login window)
main_window = tk.Tk()
main_window.title("ATM Simulator")

# Login widgets
username_label = tk.Label(main_window, text="Enter your username:")
username_entry = tk.Entry(main_window)
pin_label = tk.Label(main_window, text="Enter your PIN:")
pin_entry = tk.Entry(main_window, show="*")  # Hide PIN with asterisks
login_button = tk.Button(main_window, text="Login", command=login)

# Login widgets placement
username_label.pack()
username_entry.pack()
pin_label.pack()
pin_entry.pack()
login_button.pack()

# Initializations
users = load_users()

main_window.protocol("WM_DELETE_WINDOW", exit)  # Handle window close

main_window.mainloop()

