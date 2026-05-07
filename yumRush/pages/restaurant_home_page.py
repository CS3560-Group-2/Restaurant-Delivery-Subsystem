from tkinter import ttk
from services.db import delete_restaurant_account
from tkinter import messagebox

class RestaurantDashboardPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Restaurant Dashboard").grid(
            column=0, row=0, columnspan=2, padx=10, pady=20
        )

        ttk.Button(
            self,
            text="Edit Restaurant Info",
            command=lambda: self.controller.show_frame("RestaurantEditAccountPage")
        ).grid(column=0, row=1, padx=10, pady=10)

        ttk.Button(
            self,
            text="Edit Menu",
            command=lambda: self.controller.show_frame("MenuEditor")
        ).grid(column=0, row=2, padx=10, pady=10)

        ttk.Button(
            self,
            text="Sign Out",
            command=self.sign_out
        ).grid(column=0, row=3, padx=10, pady=10)

        ttk.Button(
            self,
            text="Delete Account",
            command=self.delete_account
        ).grid(column=0, row=4, padx=10, pady=10)

    def sign_out(self):
        self.controller.current_restaurant = None
        self.controller.show_frame("HomePage")

    def delete_account(self) -> None:
        restaurant = self.controller.current_restaurant

        if restaurant is None:
            messagebox.showerror("Error", "No restaurant is signed in.")
            return

        confirm = messagebox.askyesno(
            "Delete Account",
            "Are you sure you want to permanently delete this restaurant account?"
        )

        if not confirm:
            return

        try:
            delete_restaurant_account(restaurant["RestaurantID"])
            self.controller.current_restaurant = None

            messagebox.showinfo("Success", "Restaurant account deleted.")
            self.controller.show_frame("HomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
