import tkinter as tk
from tkinter import ttk, messagebox
from services.db import (
    delete_customer_account,
    get_all_restaurants,
    get_menu_items_by_restaurant
)


class CustomerHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.controller = controller
        self.selected_restaurant = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ttk.Label(self, text="Customer Dashboard")
        title.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # LEFT: restaurant list
        restaurant_panel = ttk.Frame(main_frame)
        restaurant_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(
            restaurant_panel,
            text="Restaurants"
        ).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(restaurant_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            restaurant_panel,
            orient="vertical",
            command=canvas.yview
        )

        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(self.canvas_window, width=e.width)
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # RIGHT: menu panel
        menu_panel = ttk.Frame(main_frame, padding=10, relief="ridge")
        menu_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ttk.Label(
            menu_panel,
            text="Menu"
        ).pack(anchor="w", pady=(0, 10))

        self.selected_label = ttk.Label(
            menu_panel,
            text="Select a restaurant to view its menu."
        )
        self.selected_label.pack(anchor="w", pady=(0, 10))

        self.menu_table = ttk.Treeview(
            menu_panel,
            columns=("name", "cost"),
            show="headings",
            height=15
        )

        self.menu_table.heading("name", text="Item")
        self.menu_table.heading("cost", text="Cost")

        self.menu_table.column("name", width=180)
        self.menu_table.column("cost", width=80)

        self.menu_table.pack(fill="both", expand=True)

        # Bottom nav
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Edit Account",
            command=lambda: controller.show_frame("CustomerEditAccountPage")
        ).pack(side="left")

        ttk.Button(
            bottom_bar,
            text="Order History",
            command=lambda: controller.show_frame("CustomerOrderHistoryPage")
        ).pack(side="left", padx=10)

        ttk.Button(
            bottom_bar,
            text="Delete Account",
            command=self.delete_account
        ).pack(side="left", padx=10)

        ttk.Button(
            bottom_bar,
            text="Sign Out",
            command=self.sign_out
        ).pack(side="right")

    def on_show(self) -> None:
        self.load_restaurants()

    def load_restaurants(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            restaurants = get_all_restaurants()

            if not restaurants:
                ttk.Label(
                    self.scrollable_frame,
                    text="No restaurants available."
                ).pack(anchor="w", padx=10, pady=10)
                return

            for restaurant in restaurants:
                self.create_restaurant_card(restaurant)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def create_restaurant_card(self, restaurant: dict) -> None:
        card = ttk.Frame(
            self.scrollable_frame,
            padding=12,
            relief="ridge",
            borderwidth=1
        )
        card.pack(fill="x", expand=True, padx=10, pady=8)

        card.grid_columnconfigure(0, weight=1)

        name_label = ttk.Label(
            card,
            text=restaurant["Name"],
            font=("Arial", 14, "bold")
        )
        name_label.grid(row=0, column=0, sticky="w")

        # Placeholder until restaurant ratings are implemented
        rating_label = ttk.Label(
            card,
            text="Rating: ★★★★☆ 4/5"
        )
        rating_label.grid(row=1, column=0, sticky="w", pady=2)

        ttk.Button(
            card,
            text="View Menu",
            command=lambda r=restaurant: self.select_restaurant(r)
        ).grid(row=0, column=1, rowspan=2, padx=10, sticky="e")

        ttk.Button(
            card,
            text="Order",
            command=lambda r=restaurant: self.start_order(r)
        ).grid(row=0, column=2, rowspan=2, padx=10, sticky="e")

    def select_restaurant(self, restaurant: dict) -> None:
        self.selected_restaurant = restaurant

        self.selected_label.config(
            text=f'Menu for: {restaurant["Name"]}'
        )

        self.load_menu_items(restaurant["RestaurantID"])

    def load_menu_items(self, restaurant_id: int) -> None:
        for row in self.menu_table.get_children():
            self.menu_table.delete(row)

        try:
            menu_items = get_menu_items_by_restaurant(restaurant_id)

            if not menu_items:
                self.menu_table.insert(
                    "",
                    "end",
                    values=("No menu items yet", "")
                )
                return

            for item in menu_items:
                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        item["Name"],
                        f'${item["Cost"]}'
                    )
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def sign_out(self) -> None:
        self.controller.current_customer = None
        self.selected_restaurant = None
        self.controller.show_frame("HomePage")

    def delete_account(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            return

        confirm = messagebox.askyesno(
            "Delete Account",
            "Are you sure you want to permanently delete your customer account?"
        )

        if not confirm:
            return

        try:
            delete_customer_account(customer["CustomerID"])
            self.controller.current_customer = None
            self.selected_restaurant = None
            messagebox.showinfo("Success", "Customer account deleted successfully.")
            self.controller.show_frame("HomePage")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def start_order(self, restaurant: dict) -> None:
        self.controller.current_order_restaurant = restaurant
        self.controller.show_frame("CustomerOrderPage")
