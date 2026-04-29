from tkinter import messagebox
import ttkbootstrap as ttk
from services.db import update_customer_info


class CustomerEditAccountPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Edit Customer Account").grid(
            column=0, row=0, columnspan=2, padx=10, pady=15
        )

        ttk.Label(self, text="Name").grid(column=0, row=1, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self, text="Username").grid(column=0, row=2, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self, text="Street").grid(column=0, row=3, padx=10, pady=5, sticky="w")
        self.street_entry = ttk.Entry(self)
        self.street_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(self, text="City").grid(column=0, row=4, padx=10, pady=5, sticky="w")
        self.city_entry = ttk.Entry(self)
        self.city_entry.grid(column=1, row=4, padx=10, pady=5)

        ttk.Label(self, text="State").grid(column=0, row=5, padx=10, pady=5, sticky="w")
        self.state_entry = ttk.Entry(self)
        self.state_entry.grid(column=1, row=5, padx=10, pady=5)

        ttk.Label(self, text="Zip Code").grid(column=0, row=6, padx=10, pady=5, sticky="w")
        self.zip_entry = ttk.Entry(self)
        self.zip_entry.grid(column=1, row=6, padx=10, pady=5)

        ttk.Label(self, text="Country").grid(column=0, row=7, padx=10, pady=5, sticky="w")
        self.country_entry = ttk.Entry(self)
        self.country_entry.grid(column=1, row=7, padx=10, pady=5)

        ttk.Button(self, text="Save Changes", command=self.save_changes).grid(
            column=0, row=8, padx=10, pady=15
        )

        ttk.Button(self, text="Back", command=lambda: controller.show_frame("CustomerHomePage")).grid(
            column=1, row=8, padx=10, pady=15
        )

    def on_show(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            self.controller.show_frame("HomePage")
            return

        self.name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.street_entry.delete(0, "end")
        self.city_entry.delete(0, "end")
        self.state_entry.delete(0, "end")
        self.zip_entry.delete(0, "end")
        self.country_entry.delete(0, "end")

        self.name_entry.insert(0, customer["Name"] or "")
        self.username_entry.insert(0, customer["Username"] or "")
        self.street_entry.insert(0, customer["Street"] or "")
        self.city_entry.insert(0, customer["City"] or "")
        self.state_entry.insert(0, customer["State"] or "")
        self.zip_entry.insert(0, str(customer["ZIP"]) if customer["ZIP"] is not None else "")
        self.country_entry.insert(0, customer["Country"] or "")

    def save_changes(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            return

        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        street = self.street_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        zip_code = self.zip_entry.get().strip()
        country = self.country_entry.get().strip()

        if not name or not username or not street or not city or not state or not zip_code or not country:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            update_customer_info(
                customer["CustomerID"],
                name,
                username,
                street,
                city,
                state,
                int(zip_code),
                country
            )

            customer["Name"] = name
            customer["Username"] = username
            customer["Street"] = street
            customer["City"] = city
            customer["State"] = state
            customer["ZIP"] = int(zip_code)
            customer["Country"] = country

            messagebox.showinfo("Success", "Customer account updated successfully.")
            self.controller.show_frame("CustomerHomePage")

        except ValueError:
            messagebox.showerror("Error", "Zip Code must be a number.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
