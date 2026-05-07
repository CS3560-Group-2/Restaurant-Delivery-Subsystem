import tkinter as tk
from tkinter import ttk, messagebox
from services.db import update_restaurant_info, get_restaurant_by_username


class RestaurantEditAccountPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.controller = controller

        ttk.Label(
            self,
            text="Edit Restaurant Account"
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        labels = [
            "Restaurant Name",
            "Username",
            "Street",
            "City",
            "State",
            "Zip Code",
            "Country"
        ]

        self.entries = {}

        for i, label in enumerate(labels, start=1):
            ttk.Label(self, text=label).grid(
                row=i,
                column=0,
                padx=10,
                pady=5,
                sticky="e"
            )

            entry = ttk.Entry(self, width=30)
            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=5,
                sticky="w"
            )

            self.entries[label] = entry

        ttk.Button(
            self,
            text="Save Changes",
            command=self.save_changes
        ).grid(row=8, column=0, padx=10, pady=20)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("RestaurantDashboardPage")
        ).grid(row=8, column=1, padx=10, pady=20)

    def on_show(self) -> None:
        restaurant = self.controller.current_restaurant

        if restaurant is None:
            return

        self.entries["Restaurant Name"].delete(0, tk.END)
        self.entries["Restaurant Name"].insert(0, restaurant.get("Name", ""))

        self.entries["Username"].delete(0, tk.END)
        self.entries["Username"].insert(0, restaurant.get("Username", ""))

        self.entries["Street"].delete(0, tk.END)
        self.entries["Street"].insert(0, restaurant.get("Street", ""))

        self.entries["City"].delete(0, tk.END)
        self.entries["City"].insert(0, restaurant.get("City", ""))

        self.entries["State"].delete(0, tk.END)
        self.entries["State"].insert(0, restaurant.get("State", ""))

        self.entries["Zip Code"].delete(0, tk.END)
        self.entries["Zip Code"].insert(0, restaurant.get("ZIP", ""))

        self.entries["Country"].delete(0, tk.END)
        self.entries["Country"].insert(0, restaurant.get("Country", ""))

    def save_changes(self) -> None:
        restaurant = self.controller.current_restaurant

        if restaurant is None:
            messagebox.showerror("Error", "No restaurant is signed in.")
            return

        name = self.entries["Restaurant Name"].get().strip()
        username = self.entries["Username"].get().strip()
        street = self.entries["Street"].get().strip()
        city = self.entries["City"].get().strip()
        state = self.entries["State"].get().strip()
        zip_code = self.entries["Zip Code"].get().strip()
        country = self.entries["Country"].get().strip()

        if not all([name, username, street, city, state, zip_code, country]):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            update_restaurant_info(
                restaurant["RestaurantID"],
                name,
                username,
                street,
                city,
                state,
                int(zip_code),
                country
            )

            self.controller.current_restaurant = get_restaurant_by_username(username)

            messagebox.showinfo("Success", "Restaurant account updated.")
            self.controller.show_frame("RestaurantDashboardPage")

        except ValueError:
            messagebox.showerror("Error", "Zip Code must be a number.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
