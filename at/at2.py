#!/usr/bin/env python3
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

def main():
    print("Welcome to the ATM Simulator")
    users = load_users()
    attempts = 3

    while attempts > 0:
        username = input("Enter your username: ")
        pin = input("Enter your PIN: ")

        user = authenticate_user(username, pin, users)
        if user:
            print(f"Login successful, Welcome {username}!")

            while True:
                print("\nATM Options:")
                print("1. Check Balance")
                print("2. Withdraw")
                print("3. Deposit")
                print("4. Change PIN")
                print("5. Add New User")
                print("6. Exit")
                choice = input("Enter your choice (1/2/3/4/5/6): ")

                if choice == "1":
                    print(f"Account Balance: ${user['balance']:.2f}")
                elif choice == "2":
                    amount = float(input("Enter the amount to withdraw: "))
                    if amount <= 0:
                        print("Invalid amount.")
                    elif amount <= user['balance']:
                        user['balance'] -= amount
                        print(f"Withdrew ${amount:.2f}. New balance: ${user['balance']:.2f}")
                    else:
                        print("Insufficient funds.")
                elif choice == "3":
                    amount = float(input("Enter the amount to deposit: "))
                    if amount > 0:
                        user['balance'] += amount
                        print(f"Deposited ${amount:.2f}. New balance: ${user['balance']:.2f}")
                    else:
                        print("Invalid amount.")
                elif choice == "4":
                    new_pin = input("Enter your new PIN (4 characters): ")
                    if len(new_pin) == 4:
                        user['pin'] = new_pin
                        save_users(users)
                        print("PIN changed successfully.")
                    else:
                        print("Invalid PIN format (4 characters required).")
                elif choice == "5":
                    new_username = input("Enter the new username: ")
                    new_pin = input("Enter the new PIN (4 characters): ")
                    if len(new_pin) == 4:
                        if add_user(new_username, new_pin, users):
                            print("User added successfully.")
                        else:
                            print("Username already exists.")
                    else:
                        print("Invalid PIN format (4 characters required).")
                elif choice == "6":
                    print("Thank you for using ATM Simulator. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please choose again.")
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Invalid login. {attempts} attempts remaining.")
            else:
                print("Maximum login attempts reached. Goodbye!")

if __name__ == "__main__":
    main()

