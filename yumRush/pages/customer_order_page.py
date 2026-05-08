import tkinter as tk
from tkinter import ttk, messagebox
from services.db import get_menu_items_by_restaurant, create_order


class CustomerOrderPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.controller = controller
        self.restaurant = None
        self.cart = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ttk.Label(self, text="Order")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Menu table
        menu_frame = ttk.Frame(self, padding=10)
        menu_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        ttk.Label(menu_frame, text="Menu Items").pack(anchor="w")

        self.menu_table = ttk.Treeview(
            menu_frame,
            columns=("name", "cost"),
            show="headings",
            height=15
        )

        self.menu_table.heading("name", text="Item")
        self.menu_table.heading("cost", text="Cost")

        self.menu_table.column("name", width=180)
        self.menu_table.column("cost", width=80)

        self.menu_table.pack(fill="both", expand=True, pady=10)

        ttk.Button(
            menu_frame,
            text="Add to Cart",
            command=self.add_to_cart
        ).pack(anchor="e")

        # Cart table
        cart_frame = ttk.Frame(self, padding=10)
        cart_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

        ttk.Label(cart_frame, text="Cart").pack(anchor="w")

        self.cart_table = ttk.Treeview(
            cart_frame,
            columns=("name", "cost", "quantity", "subtotal"),
            show="headings",
            height=15
        )

        self.cart_table.heading("name", text="Item")
        self.cart_table.heading("cost", text="Cost")
        self.cart_table.heading("quantity", text="Qty")
        self.cart_table.heading("subtotal", text="Subtotal")

        self.cart_table.pack(fill="both", expand=True, pady=10)

        self.total_label = ttk.Label(cart_frame, text="Total: $0")
        self.total_label.pack(anchor="e")

        ttk.Button(
            cart_frame,
            text="Remove Selected",
            command=self.remove_from_cart
        ).pack(anchor="e", pady=5)

        ttk.Button(
            cart_frame,
            text="Place Order",
            command=self.place_order
        ).pack(anchor="e", pady=5)

        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=2, column=0, columnspan=2, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Back",
            command=lambda: controller.show_frame("CustomerHomePage")
        ).pack(side="left")

    def on_show(self) -> None:
        self.restaurant = self.controller.current_order_restaurant
        self.cart = []

        if self.restaurant is None:
            self.title_label.config(text="Order")
            return

        self.title_label.config(text=f'Order from {self.restaurant["Name"]}')
        self.load_menu()
        self.refresh_cart()

    def load_menu(self) -> None:
        for row in self.menu_table.get_children():
            self.menu_table.delete(row)

        menu_items = get_menu_items_by_restaurant(self.restaurant["RestaurantID"])

        for item in menu_items:
            self.menu_table.insert(
                "",
                "end",
                iid=str(item["MenuItemID"]),
                values=(item["Name"], f'${item["Cost"]}')
            )

    def add_to_cart(self) -> None:
        selected = self.menu_table.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a menu item.")
            return

        menu_item_id = int(selected[0])
        values = self.menu_table.item(selected[0], "values")

        name = values[0]
        cost = int(values[1].replace("$", ""))

        for item in self.cart:
            if item["MenuItemID"] == menu_item_id:
                item["Quantity"] += 1
                self.refresh_cart()
                return

        self.cart.append({
            "MenuItemID": menu_item_id,
            "Name": name,
            "Cost": cost,
            "Quantity": 1
        })

        self.refresh_cart()

    def remove_from_cart(self) -> None:
        selected = self.cart_table.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a cart item.")
            return

        menu_item_id = int(selected[0])

        self.cart = [
            item for item in self.cart
            if item["MenuItemID"] != menu_item_id
        ]

        self.refresh_cart()

    def refresh_cart(self) -> None:
        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        total = 0

        for item in self.cart:
            subtotal = item["Cost"] * item["Quantity"]
            total += subtotal

            self.cart_table.insert(
                "",
                "end",
                iid=str(item["MenuItemID"]),
                values=(
                    item["Name"],
                    f'${item["Cost"]}',
                    item["Quantity"],
                    f'${subtotal}'
                )
            )

        self.total_label.config(text=f"Total: ${total}")

    def place_order(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            return

        if self.restaurant is None:
            messagebox.showerror("Error", "No restaurant selected.")
            return

        if not self.cart:
            messagebox.showerror("Error", "Your cart is empty.")
            return

        try:
            order_id = create_order(
                customer["CustomerID"],
                self.restaurant["RestaurantID"],
                self.cart
            )

            messagebox.showinfo(
                "Order Placed",
                f"Order #{order_id} has been placed successfully."
            )

            self.cart = []
            self.refresh_cart()
            self.controller.show_frame("CustomerHomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
