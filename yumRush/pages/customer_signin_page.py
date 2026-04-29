from tkinter import messagebox
import ttkbootstrap as ttk
from services.db import get_customer_by_username


class CustomerSignInPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Customer Sign In").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self, text="Username").grid(column=0, row=1, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=1, padx=10, pady=5)

        ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage")).grid(
            column=0, row=2, padx=10, pady=10
        )

        ttk.Button(self, text="Sign In", command=self.handle_signin).grid(
            column=1, row=2, padx=10, pady=10
        )

    def handle_signin(self) -> None:
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        try:
            customer = get_customer_by_username(username)

            if customer is None:
                messagebox.showerror("Sign In Failed", "Customer username not found.")
                self.username_entry.delete(0, "end")
                return

            self.controller.current_customer = customer
            messagebox.showinfo("Success", f"Welcome back, {customer['Name']}!")
            self.username_entry.delete(0, "end")
            self.controller.show_frame("CustomerHomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
