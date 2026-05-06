from tkinter import ttk, messagebox
from mysql.connector import Error

from services.db import create_address, create_restaurant, get_restaurant_by_username


class RestaurantSignUpPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Restaurant Sign Up").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        self.name_entry = self.add_field("Restaurant Name", 1)
        self.username_entry = self.add_field("Username", 2)
        self.street_entry = self.add_field("Street", 3)
        self.city_entry = self.add_field("City", 4)
        self.state_entry = self.add_field("State", 5)
        self.zip_entry = self.add_field("Zip Code", 6)
        self.country_entry = self.add_field("Country", 7)

        ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage")).grid(
            column=0, row=8, padx=10, pady=10
        )

        ttk.Button(self, text="Sign Up", command=self.sign_up).grid(
            column=1, row=8, padx=10, pady=10
        )

    def add_field(self, label_text, row):
        ttk.Label(self, text=label_text).grid(column=0, row=row, padx=10, pady=5)
        entry = ttk.Entry(self)
        entry.grid(column=1, row=row, padx=10, pady=5)
        return entry

    def sign_up(self) -> None:
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        street = self.street_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        zip_code = self.zip_entry.get().strip()
        country = self.country_entry.get().strip()

        if not all([name, username, street, city, state, zip_code, country]):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if not zip_code.isdigit():
            messagebox.showerror("Error", "Zip code must be a number.")
            return

        if get_restaurant_by_username(username) is not None:
            messagebox.showerror("Error", "That username is already taken.")
            return

        try:
            address_id = create_address(street, city, state, int(zip_code), country)
            restaurant_id = create_restaurant(name, username, address_id)

            restaurant = get_restaurant_by_username(username)
            self.controller.current_restaurant = restaurant

            messagebox.showinfo("Success", f"Restaurant account created. ID: {restaurant_id}")
            self.controller.show_frame("MenuEditor")

        except Error as e:
            messagebox.showerror("Database Error", str(e))
