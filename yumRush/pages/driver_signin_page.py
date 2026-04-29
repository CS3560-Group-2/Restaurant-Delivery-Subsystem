from tkinter import ttk, messagebox
from services.db import get_driver_by_username


class DriverSignInPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Driver Sign In").grid(column=0, row=2, padx=10, pady=10)

        ttk.Label(self, text="Username").grid(column=0, row=3, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(
            self,
            text="Back",
            command=self.goBack 
            ).grid(column=0, row=5, padx=10, pady=10)

        ttk.Button(
            self,
            text="Sign in",
            command=self.handle_signin
        ).grid(column=1, row=5, padx=10, pady=10)
    def goBack(self) -> None:
        self.controller.show_frame("HomePage")
        self.username_entry.delete(0, "end")

    def handle_signin(self) -> None:
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        try:
            driver = get_driver_by_username(username)

            if driver is None:
                messagebox.showerror("Sign In Failed", "Driver username not found.")
                return

            messagebox.showinfo("Success", f"Welcome back, {driver['Name']}!")
            self.controller.show_frame("DriverHomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        self.username_entry.delete(0, "end")
