from tkinter import ttk, messagebox
from services.db import create_driver

class DriverSignUpPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Driver Sign Up").grid(column=0, row=2, padx=10, pady=10)

        ttk.Label(self, text="First Name").grid(column=0, row=3, padx=10, pady=5)
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(self, text="Last Name").grid(column=0, row=4, padx=10, pady=5)
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(column=1, row=4, padx=10, pady=5)

        ttk.Label(self, text="License Plate Number").grid(column=0, row=5, padx=10, pady=5)
        self.license_plate_entry = ttk.Entry(self)
        self.license_plate_entry.grid(column=1, row=5, padx=10, pady=5)

        ttk.Label(self, text="Username").grid(column=0, row=6, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=6, padx=10, pady=5)

        ttk.Button(self, text="Sign Up", command=self.handle_signup).grid(
            column=1, row=7, padx=10, pady=10
        )

        ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage")).grid(
            column=0, row=7, padx=10, pady=10
        )

    def handle_signup(self) -> None:
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        license_plate = self.license_plate_entry.get().strip()
        username = self.username_entry.get().strip()

        if not first_name or not last_name or not license_plate or not username:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        full_name = f"{first_name} {last_name}"

        try:
            create_driver(full_name, username, license_plate)
            messagebox.showinfo("Success", "Driver account created successfully.")

            self.first_name_entry.delete(0, "end")
            self.last_name_entry.delete(0, "end")
            self.license_plate_entry.delete(0, "end")
            self.username_entry.delete(0, "end")

            self.controller.show_frame("HomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
