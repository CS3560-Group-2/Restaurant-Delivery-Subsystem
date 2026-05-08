import tkinter as tk
from tkinter import ttk


class OrderHistoryFrame(ttk.Frame):

    abstract_page = True


    def __init__(self, parent, controller, back_page: str) -> None:
        super().__init__(parent)

        self.controller = controller
        self.back_page = back_page

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ttk.Label(
            self,
            text="Order History",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, padx=20, pady=20)

        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas_window, width=e.width)
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Back",
            command=lambda: controller.show_frame(self.back_page)
        ).pack(side="left")

    def load_orders(self, orders: list[dict]) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not orders:
            ttk.Label(
                self.scrollable_frame,
                text="No orders found."
            ).pack(anchor="w", padx=10, pady=10)
            return

        for order in orders:
            self.create_order_card(order)

    def create_order_card(self, order: dict) -> None:
        card = ttk.Frame(
            self.scrollable_frame,
            padding=12,
            relief="ridge",
            borderwidth=1
        )
        card.pack(fill="x", expand=True, padx=10, pady=8)

        card.grid_columnconfigure(0, weight=1)

        date_text = order.get("CreatedAt", "Unknown date")
        restaurant_name = order.get("RestaurantName", "Unknown restaurant")
        total = order.get("TotalCost", 0)
        status = order.get("Status", "Unknown")

        ttk.Label(
            card,
            text=f"Order #{order['OrderID']}",
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            card,
            text=f"Restaurant: {restaurant_name}"
        ).grid(row=1, column=0, sticky="w", pady=2)

        ttk.Label(
            card,
            text=f"Date: {date_text}"
        ).grid(row=2, column=0, sticky="w", pady=2)

        ttk.Label(
            card,
            text=f"Total: ${total}"
        ).grid(row=3, column=0, sticky="w", pady=2)

        ttk.Label(
            card,
            text=f"Status: {status}"
        ).grid(row=4, column=0, sticky="w", pady=2)

        ttk.Button(
            card,
            text="View Details",
            command=lambda o=order: self.open_order_details(o)
        ).grid(row=0, column=1, rowspan=5, padx=10, sticky="e")

    def open_order_details(self, order: dict) -> None:
        self.controller.current_order_id = order["OrderID"]
        self.controller.previous_order_history_page = self.__class__.__name__
        self.controller.show_frame("OrderDetailPage")
