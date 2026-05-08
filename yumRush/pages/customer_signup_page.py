from tkinter import messagebox
import ttkbootstrap as ttk
from services.db import create_customer, get_customer_by_username


class CustomerSignUpPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Customer Sign Up").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self, text="Customer Name").grid(column=0, row=1, padx=10, pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self, text="Username").grid(column=0, row=2, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self, text="Street").grid(column=0, row=3, padx=10, pady=5)
        self.street_entry = ttk.Entry(self)
        self.street_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(self, text="City").grid(column=0, row=4, padx=10, pady=5)
        self.city_entry = ttk.Entry(self)
        self.city_entry.grid(column=1, row=4, padx=10, pady=5)

        ttk.Label(self, text="State").grid(column=0, row=5, padx=10, pady=5)
        self.state_entry = ttk.Entry(self)
        self.state_entry.grid(column=1, row=5, padx=10, pady=5)

        ttk.Label(self, text="Zip Code").grid(column=0, row=6, padx=10, pady=5)
        self.zip_entry = ttk.Entry(self)
        self.zip_entry.grid(column=1, row=6, padx=10, pady=5)

        ttk.Label(self, text="Country").grid(column=0, row=7, padx=10, pady=5)
        self.country_entry = ttk.Entry(self)
        self.country_entry.grid(column=1, row=7, padx=10, pady=5)

        ttk.Button(self, text="add payment method", command=self.handle_signup).grid(
            column=1, row=8, padx=10, pady=10
        )

        ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage")).grid(
            column=0, row=8, padx=10, pady=10
        )

    def handle_signup(self) -> None:
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        street = self.street_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        zip_code = self.zip_entry.get().strip()
        country = self.country_entry.get().strip()

        if not name or not username or not street or not city or not state or not zip_code or not country:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            create_customer(name, username, street, city, state, int(zip_code), country)
            
            customer = get_customer_by_username(username)
            self.controller.current_customer = customer

            self.name_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.street_entry.delete(0, "end")
            self.city_entry.delete(0, "end")
            self.state_entry.delete(0, "end")
            self.zip_entry.delete(0, "end")
            self.country_entry.delete(0, "end")

            self.controller.show_frame("CustomerPaymentMethodsPage")

        except ValueError:
            messagebox.showerror("Error", "Zip Code must be a number.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
