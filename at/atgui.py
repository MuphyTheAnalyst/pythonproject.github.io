#!/usr/bin/env python3
import json
import tkinter as tk
from tkinter import messagebox

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

# Function to handle deposit
def deposit():
    global amount_entry, user, users

    try:
        amount = float(amount_entry.get())
        if amount > 0:
            user['balance'] += amount
            save_users(users)
            messagebox.showinfo("Deposit", f"Deposited ${amount:.2f}. New balance: ${user['balance']:.2f}")
        else:
            messagebox.showerror("Error", "Invalid amount.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")

# Create the main window
root = tk.Tk()
root.title("ATM Simulator")

# Load user data
users = load_users()
attempts = 3
user = None  # To store the authenticated user

# Create the login frame
login_frame = tk.Frame(root)
login_frame.pack()

# Create login widgets
username_label = tk.Label(login_frame, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

pin_label = tk.Label(login_frame, text="PIN:")
pin_label.pack()
pin_entry = tk.Entry(login_frame, show="*")  # Mask the PIN
pin_entry.pack()

# Create login button
def login():
    global attempts, user
    username = username_entry.get()
    pin = pin_entry.get()

    user = authenticate_user(username, pin, users)
    if user:
        login_frame.pack_forget()
        create_atm_interface()
    else:
        attempts -= 1
        if attempts > 0:
            messagebox.showerror("Error", f"Invalid login. {attempts} attempts remaining.")
        else:
            messagebox.showerror("Error", "Maximum login attempts reached. Goodbye!")
            root.destroy()

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

def create_atm_interface():
    atm_frame = tk.Frame(root)
    atm_frame.pack()

    def check_balance():
        if user:
            messagebox.showinfo("Account Balance", f"Account Balance: ${user['balance']:.2f}")
        else:
            messagebox.showerror("Error", "User not authenticated.")

    def withdraw():
        global amount_entry
        amount_entry = tk.Entry(atm_frame)
        amount_entry.pack()

        withdraw_button = tk.Button(atm_frame, text="Withdraw", command=perform_withdraw)
        withdraw_button.pack()

    def perform_withdraw():
        if user:
            try:
                amount = float(amount_entry.get())
                if amount > 0:
                    if amount <= user['balance']:
                        user['balance'] -= amount
                        save_users(users)
                        messagebox.showinfo("Withdraw", f"Withdrew ${amount:.2f}. New balance: ${user['balance']:.2f}")
                    else:
                        messagebox.showerror("Error", "Insufficient funds.")
                else:
                    messagebox.showerror("Error", "Invalid amount.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "User not authenticated.")

    def exit_atm():
        root.destroy()

    check_balance_button = tk.Button(atm_frame, text="Check Balance", command=check_balance)
    withdraw_button = tk.Button(atm_frame, text="Withdraw", command=withdraw)
    deposit_button = tk.Button(atm_frame, text="Deposit", command=deposit)
    change_pin_button = tk.Button(atm_frame, text="Change PIN", command=change_pin)
    add_new_user_button = tk.Button(atm_frame, text="Add New User", command=add_new_user)
    exit_button = tk.Button(atm_frame, text="Exit", command=exit_atm)

    check_balance_button.pack()
    withdraw_button.pack()
    deposit_button.pack()
    change_pin_button.pack()
    add_new_user_button.pack()
    exit_button.pack()

# Start the application
root.mainloop()

