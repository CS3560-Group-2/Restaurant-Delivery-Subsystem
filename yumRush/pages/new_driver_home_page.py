from tkinter import ttk, messagebox

from services.db import (
    get_assigned_order_for_driver,
    mark_order_delivered,
    update_driver_status,
)


class DriverHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.current_order = None

        self.status_options = ["unavailable", "On route", "available", "arrived"]

        ttk.Label(self, text="Driver Dashboard").grid(
            column=0, row=0, columnspan=2, padx=10, pady=10
        )

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
        self.status_dropdown.grid(column=0, row=5, padx=10, pady=10)

        ttk.Button(self, text="Update Status", command=self.confirm_status).grid(
            column=1, row=5, padx=10, pady=10
        )

        order_frame = ttk.LabelFrame(self, text="Assigned Order", padding=15)
        order_frame.grid(column=0, row=6, columnspan=2, padx=10, pady=15, sticky="ew")

        self.order_id_label = ttk.Label(order_frame, text="Order ID: -")
        self.order_id_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        self.order_status_label = ttk.Label(order_frame, text="Order Status: -")
        self.order_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Label(order_frame, text="Restaurant Address:").grid(
            row=2, column=0, sticky="nw", pady=8
        )
        self.restaurant_address_label = ttk.Label(order_frame, text="-", wraplength=450)
        self.restaurant_address_label.grid(row=2, column=1, sticky="w", pady=8)

        ttk.Label(order_frame, text="Customer Address:").grid(
            row=3, column=0, sticky="nw", pady=8
        )
        self.customer_address_label = ttk.Label(order_frame, text="-", wraplength=450)
        self.customer_address_label.grid(row=3, column=1, sticky="w", pady=8)

        self.delivered_button = ttk.Button(
            order_frame,
            text="Mark Order as Delivered",
            command=self.mark_delivered,
        )
        self.delivered_button.grid(row=4, column=1, sticky="e", pady=15)

        ttk.Button(self, text="Refresh Order", command=self.load_assigned_order).grid(
            column=0, row=7, padx=10, pady=10
        )

        ttk.Button(self, text="Sign out", command=self.sign_out).grid(
            column=1, row=7, padx=10, pady=10
        )

    def on_show(self) -> None:
        driver = self.controller.current_driver

        if driver is None:
            self.name_value.config(text="Not signed in")
            self.username_value.config(text="-")
            self.license_value.config(text="-")
            self.status_display.config(text="-")
            self.clear_order_display()
            return

        self.name_value.config(text=driver["Name"])
        self.username_value.config(text=driver["Username"])
        self.license_value.config(text=driver["LicensePlate"])
        self.status_display.config(text=driver["Status"] if driver["Status"] else "unavailable")
        self.status_dropdown.set("Set Status")

        self.load_assigned_order()

    def load_assigned_order(self) -> None:
        driver = self.controller.current_driver

        if driver is None:
            self.clear_order_display()
            return

        self.current_order = get_assigned_order_for_driver(driver["DriverID"])

        if self.current_order is None:
            self.clear_order_display("No assigned order.")
            return

        order = self.current_order

        restaurant_address = self.format_address(
            order["RestaurantStreet"],
            order["RestaurantCity"],
            order["RestaurantState"],
            order["RestaurantZIP"],
            order["RestaurantCountry"],
        )

        customer_address = self.format_address(
            order["CustomerStreet"],
            order["CustomerCity"],
            order["CustomerState"],
            order["CustomerZIP"],
            order["CustomerCountry"],
        )

        self.order_id_label.config(text=f"Order ID: {order['OrderID']}")
        self.order_status_label.config(text=f"Order Status: {order['Status']}")
        self.restaurant_address_label.config(
            text=f"{order['RestaurantName']}\n{restaurant_address}"
        )
        self.customer_address_label.config(
            text=f"{order['CustomerName']}\n{customer_address}"
        )
        self.delivered_button.config(state="normal")

    def clear_order_display(self, message: str = "-") -> None:
        self.current_order = None
        self.order_id_label.config(text=f"Order ID: {message}")
        self.order_status_label.config(text="Order Status: -")
        self.restaurant_address_label.config(text="-")
        self.customer_address_label.config(text="-")
        self.delivered_button.config(state="disabled")

    def mark_delivered(self) -> None:
        if self.current_order is None or self.controller.current_driver is None:
            return

        mark_order_delivered(
            self.current_order["OrderID"],
            self.controller.current_driver["DriverID"],
        )

        self.controller.current_driver["Status"] = "available"
        self.status_display.config(text="available")
        messagebox.showinfo("Order Delivered", "Order marked as delivered.")
        self.load_assigned_order()

    def confirm_status(self) -> None:
        selected_status = self.status_dropdown.get().strip()

        if not selected_status or selected_status == "Set Status":
            return

        self.status_display.config(text=selected_status)

        if self.controller.current_driver is not None:
            driver_id = self.controller.current_driver["DriverID"]
            update_driver_status(driver_id, selected_status)
            self.controller.current_driver["Status"] = selected_status

    def sign_out(self) -> None:
        self.controller.current_driver = None
        self.controller.show_frame("HomePage")

    def format_address(self, street, city, state, zip_code, country) -> str:
        return f"{street}, {city}, {state} {zip_code}, {country}"
