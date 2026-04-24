import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, ttk

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Delivery System")
        self.root.geometry("750x550")

        # temporary account storage
        self.users = {"admin": "123"}

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_header(self):
        tk.Label(
            self.root,
            text="Restaurant Delivery System",
            font=("Arial", 22, "bold"),
            bg="#d9e6ff"
        ).pack(fill="x", pady=10)

    def show_login(self):
        self.clear_window()
        self.show_header()

        tk.Label(self.root, text="Sign In", font=("Arial", 20, "bold")).pack(pady=30)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Sign In", width=15, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Sign Up", width=15, command=self.show_signup).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            messagebox.showinfo("Success", "Login successful.")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_signup(self):
        self.clear_window()
        self.show_header()

        tk.Label(self.root, text="Sign Up", font=("Arial", 20, "bold")).pack(pady=30)

        tk.Label(self.root, text="New Username").pack()
        self.new_username_entry = tk.Entry(self.root, width=30)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="New Password").pack()
        self.new_password_entry = tk.Entry(self.root, width=30, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Button(self.root, text="Create Account", width=15, command=self.signup).pack(pady=10)
        tk.Button(self.root, text="Back to Login", width=15, command=self.show_login).pack()

    def signup(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return

        self.users[username] = password
        messagebox.showinfo("Success", "Account created successfully.")
        self.show_login()

    def show_dashboard(self):
        self.clear_window()
        self.show_header()

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold")).pack(pady=40)

        tk.Button(self.root, text="Register New Driver", width=25, height=2,
                  command=self.show_register_driver).pack(pady=10)

        tk.Button(self.root, text="Deactivate Driver", width=25, height=2,
                  command=self.deactivate_driver).pack(pady=10)

        tk.Button(self.root, text="View Overdue Tickets", width=25, height=2,
                  command=self.show_overdue_tickets).pack(pady=10)

        tk.Button(self.root, text="Logout", width=25, height=2,
                  command=self.show_login).pack(pady=10)

    def show_register_driver(self):
        self.clear_window()
        self.show_header()

        tk.Label(self.root, text="Register New Driver", font=("Arial", 20, "bold")).pack(pady=25)

        form = tk.Frame(self.root)
        form.pack(pady=10)

        labels = ["Driver Name", "Phone Number", "Email", "License Number", "Vehicle Type"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label + ":", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(form, width=35)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries[label] = entry

        tk.Button(self.root, text="Submit", width=15, bg="#d5e8d4",
                  command=self.register_driver).pack(pady=15)

        tk.Button(self.root, text="Back", width=15,
                  command=self.show_dashboard).pack()

    def register_driver(self):
        name = self.entries["Driver Name"].get()
        phone = self.entries["Phone Number"].get()
        email = self.entries["Email"].get()
        license_number = self.entries["License Number"].get()

        if not name or not phone or not email or not license_number:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        messagebox.showinfo("Success", "Driver profile created successfully.")

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def deactivate_driver(self):
        driver_id = simpledialog.askstring("Deactivate Driver", "Enter Driver ID:")
        if driver_id:
            messagebox.showinfo("Success", f"Driver {driver_id} has been deactivated.")

    def show_overdue_tickets(self):
        self.clear_window()
        self.show_header()

        tk.Label(self.root, text="Overdue Delivery Tickets", font=("Arial", 20, "bold")).pack(pady=25)

        columns = ("Order ID", "Customer", "Driver", "Status", "Time Open", "Action")
        table = ttk.Treeview(self.root, columns=columns, show="headings", height=6)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=110)

        sample_data = [
            ("1023", "John Smith", "Mike Lee", "Overdue", "65 min", "Close"),
            ("1024", "Anna Brown", "David Tran", "Overdue", "72 min", "Escalate"),
            ("1025", "Carlos Nguyen", "Lisa Park", "Overdue", "80 min", "Close")
        ]

        for row in sample_data:
            table.insert("", tk.END, values=row)

        table.pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Close Ticket", width=15, bg="#d5e8d4",
                  command=lambda: messagebox.showinfo("Success", "Ticket closed successfully.")
                  ).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Escalate Ticket", width=15, bg="#fff2cc",
                  command=lambda: messagebox.showinfo("Success", "Ticket escalated successfully.")
                  ).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="Back", width=15, bg="#f8cecc",
                  command=self.show_dashboard).grid(row=0, column=2, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()