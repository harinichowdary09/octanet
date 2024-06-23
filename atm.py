import tkinter as tk
from tkinter import messagebox

class User:
    def _init_(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)

class AuthScreen(tk.Frame):
    def _init_(self, atm):
        super()._init_(atm.root)
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="User ID").pack()
        self.user_id_entry = tk.Entry(self)
        self.user_id_entry.pack()

        tk.Label(self, text="PIN").pack()
        self.pin_entry = tk.Entry(self, show="*")
        self.pin_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack()

    def login(self):
        user_id = self.user_id_entry.get()
        pin = self.pin_entry.get()
        self.atm.authenticate_user(user_id, pin)

class MainMenuScreen(tk.Frame):
    def _init_(self, atm):
        super()._init_(atm.root)
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ATM Main Menu").pack()

        tk.Button(self, text="View Transaction History", command=self.view_transaction_history).pack()
        tk.Button(self, text="Withdraw", command=self.withdraw).pack()
        tk.Button(self, text="Deposit", command=self.deposit).pack()
        tk.Button(self, text="Transfer", command=self.transfer).pack()
        tk.Button(self, text="Logout", command=self.logout).pack()

    def view_transaction_history(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_transaction_history()

    def withdraw(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_withdraw()

    def deposit(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_deposit()

    def transfer(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_transfer()

    def logout(self):
        self.atm.logout()

class TransactionScreen(tk.Frame):
    def _init_(self, atm):
        super()._init_(atm.root)
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Submit", command=self.submit)
        self.button.pack()

        self.back_button = tk.Button(self, text="Back", command=self.back_to_main_menu)
        self.back_button.pack()

    def show_transaction_history(self):
        self.label.config(text="Transaction History")
        self.entry.pack_forget()
        self.button.pack_forget()

        if self.atm.current_user.transaction_history:
            history = "\n".join(self.atm.current_user.transaction_history)
        else:
            history = "No transactions yet."
        messagebox.showinfo("Transaction History", history)

    def show_withdraw(self):
        self.label.config(text="Enter amount to withdraw")
        self.entry.pack()
        self.button.pack()

    def show_deposit(self):
        self.label.config(text="Enter amount to deposit")
        self.entry.pack()
        self.button.pack()

    def show_transfer(self):
        self.label.config(text="Enter user ID to transfer to and amount (separated by a space)")
        self.entry.pack()
        self.button.pack()

    def submit(self):
        action = self.label.cget("text")
        if action == "Enter amount to withdraw":
            amount = int(self.entry.get())
            if self.atm.current_user.balance >= amount:
                self.atm.current_user.balance -= amount
                self.atm.current_user.add_transaction(f"Withdraw: {amount}")
                messagebox.showinfo("Success", "Withdrawal successful")
            else:
                messagebox.showerror("Error", "Insufficient funds")
        elif action == "Enter amount to deposit":
            amount = int(self.entry.get())
            self.atm.current_user.balance += amount
            self.atm.current_user.add_transaction(f"Deposit: {amount}")
            messagebox.showinfo("Success", "Deposit successful")
        elif action == "Enter user ID to transfer to and amount (separated by a space)":
            user_id, amount = self.entry.get().split()
            amount = int(amount)
            if self.atm.current_user.balance >= amount:
                recipient = self.atm.users.get(user_id)
                if recipient:
                    self.atm.current_user.balance -= amount
                    recipient.balance += amount
                    self.atm.current_user.add_transaction(f"Transfer to {user_id}: {amount}")
                    recipient.add_transaction(f"Transfer from {self.atm.current_user.user_id}: {amount}")
                    messagebox.showinfo("Success", "Transfer successful")
                else:
                    messagebox.showerror("Error", "Recipient not found")
            else:
                messagebox.showerror("Error", "Insufficient funds")
        self.entry.delete(0, tk.END)

    def back_to_main_menu(self):
        self.atm.show_main_menu_screen()

class ATM:
    def _init_(self, root):
        self.root = root
        self.root.title("ATM System")
        self.users = self.load_users()
        self.current_user = None

        self.auth_screen = AuthScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.transaction_screen = TransactionScreen(self)

        self.auth_screen.pack()

    def load_users(self):
        # Load users from a data source (here we create some dummy users)
        return {
            'user1': User('user1', '1234', 5000),
            'user2': User('user2', '5678', 10000),
        }

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            self.current_user = user
            self.show_main_menu_screen()
        else:
            messagebox.showerror("Error", "Invalid user ID or PIN")

    def show_auth_screen(self):
        self.auth_screen.pack()
        self.main_menu_screen.pack_forget()
        self.transaction_screen.pack_forget()

    def show_main_menu_screen(self):
        self.auth_screen.pack_forget()
        self.main_menu_screen.pack()
        self.transaction_screen.pack_forget()

    def show_transaction_screen(self):
        self.auth_screen.pack_forget()
        self.main_menu_screen.pack_forget()
        self.transaction_screen.pack()

    def logout(self):
        self.current_user = None
        self.show_auth_screen()

if _name_ == "_main_":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
