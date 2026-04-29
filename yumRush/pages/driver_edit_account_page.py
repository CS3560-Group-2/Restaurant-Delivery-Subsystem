from tkinter import messagebox
import ttkbootstrap as ttk
from services.db import update_driver_info


class DriverEditAccountPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Edit Driver Account", font=("Helvetica", 18, "bold")).grid(
            column=0, row=0, columnspan=2, padx=10, pady=20
        )

        ttk.Label(self, text="Full Name").grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self, text="Username").grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(self, text="License Plate").grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.license_entry = ttk.Entry(self)
        self.license_entry.grid(column=1, row=3, padx=10, pady=10)

        ttk.Button(
            self,
            text="Save Changes",
            bootstyle="success",
            command=self.save_changes
        ).grid(column=0, row=4, padx=10, pady=20)

        ttk.Button(
            self,
            text="Back",
            bootstyle="secondary",
            command=lambda: self.controller.show_frame("DriverHomePage")
        ).grid(column=1, row=4, padx=10, pady=20)

    def on_show(self) -> None:
        driver = self.controller.current_driver

        if driver is None:
            messagebox.showerror("Error", "No driver is signed in.")
            self.controller.show_frame("HomePage")
            return

        self.name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.license_entry.delete(0, "end")

        self.name_entry.insert(0, driver["Name"])
        self.username_entry.insert(0, driver["Username"])
        self.license_entry.insert(0, driver["LicensePlate"])

    def save_changes(self) -> None:
        driver = self.controller.current_driver

        if driver is None:
            messagebox.showerror("Error", "No driver is signed in.")
            return

        new_name = self.name_entry.get().strip()
        new_username = self.username_entry.get().strip()
        new_license = self.license_entry.get().strip()

        if not new_name or not new_username or not new_license:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            update_driver_info(
                driver["DriverID"],
                new_name,
                new_username,
                new_license
            )

            driver["Name"] = new_name
            driver["Username"] = new_username
            driver["LicensePlate"] = new_license

            messagebox.showinfo("Success", "Account updated successfully.")
            self.controller.show_frame("DriverHomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
