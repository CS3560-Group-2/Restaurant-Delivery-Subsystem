from tkinter import ttk


class DriverHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        self.status_options = ["unavailable", "On route", "available", "arrived"]

        ttk.Label(self, text="Driver Home Page").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self, text="Name:").grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.name_value = ttk.Label(self, text="Not signed in")
        self.name_value.grid(column=1, row=1, sticky="w", padx=10, pady=5)

        ttk.Label(self, text="Username:").grid(column=0, row=2, sticky="w", padx=10, pady=5)
        self.username_value = ttk.Label(self, text="-")
        self.username_value.grid(column=1, row=2, sticky="w", padx=10, pady=5)

        ttk.Label(self, text="License Plate:").grid(column=0, row=3, sticky="w", padx=10, pady=5)
        self.license_value = ttk.Label(self, text="-")
        self.license_value.grid(column=1, row=3, sticky="w", padx=10, pady=5)

        ttk.Label(self, text="Current Status:").grid(column=0, row=4, sticky="w", padx=10, pady=5)
        self.status_display = ttk.Label(self, text="-")
        self.status_display.grid(column=1, row=4, sticky="w", padx=10, pady=5)

        self.status_dropdown = ttk.Combobox(self, values=self.status_options, state="readonly")
        self.status_dropdown.set("Set Status")
        self.status_dropdown.grid(column=0, row=5, padx=10, pady=20)

        ttk.Button(
            self,
            text="Status Update",
            command=self.confirm_status
        ).grid(column=1, row=5, padx=10, pady=20)

        ttk.Button(
            self,
            text="Sign out",
            command=self.sign_out
        ).grid(column=0, row=6, padx=10, pady=10)

    def on_show(self) -> None:
        driver = self.controller.current_driver

        if driver is None:
            self.name_value.config(text="Not signed in")
            self.username_value.config(text="-")
            self.license_value.config(text="-")
            self.status_display.config(text="-")
            self.status_dropdown.set("Set Status")
            return

        self.name_value.config(text=driver["Name"])
        self.username_value.config(text=driver["Username"])
        self.license_value.config(text=driver["LicensePlate"])
        self.status_display.config(text=driver["Status"] if driver["Status"] else "unavailable")
        self.status_dropdown.set("Set Status")

    def confirm_status(self) -> None:
        selected_status = self.status_dropdown.get().strip()

        if not selected_status or selected_status == "Set Status":
            return

        self.status_display.config(text=selected_status)

        if self.controller.current_driver is not None:
            self.controller.current_driver["Status"] = selected_status

    def sign_out(self) -> None:
        self.controller.current_driver = None
        self.controller.show_frame("HomePage")
