import tkinter as tk
from tkinter import ttk, messagebox
from services.db import get_restaurant_by_username


class RestaurantSignInPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
      
        ttk.Label(self, text="Restaurant Sign In").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self, text="Username").grid(column=0, row=1, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=1, padx=10, pady=5)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("HomePage")
        ).grid(column=0, row=2, padx=10, pady=10)

        ttk.Button(
            self,
            text="Sign In",
            command=self.sign_in
        ).grid(column=1, row=2, padx=10, pady=10)

    def sign_in(self) -> None:
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        restaurant = get_restaurant_by_username(username)

        if restaurant is None:
            messagebox.showerror("Error", "Restaurant account not found.")
            return

        self.controller.current_restaurant = restaurant
        self.controller.show_frame("RestaurantDashboardPage")
