from tkinter import ttk, messagebox
from services.db import get_order_details


class OrderDetailPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title_label = ttk.Label(
            self,
            text="Order Details",
            font=("Arial", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.info_label = ttk.Label(self, text="")
        self.info_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.items_table = ttk.Treeview(
            self,
            columns=("name", "cost", "quantity", "subtotal"),
            show="headings"
        )

        self.items_table.heading("name", text="Item")
        self.items_table.heading("cost", text="Cost")
        self.items_table.heading("quantity", text="Qty")
        self.items_table.heading("subtotal", text="Subtotal")

        self.items_table.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Back",
            command=self.go_back
        ).pack(side="left")

    def on_show(self) -> None:
        order_id = self.controller.current_order_id

        if order_id is None:
            messagebox.showerror("Error", "No order selected.")
            return

        for row in self.items_table.get_children():
            self.items_table.delete(row)

        try:
            data = get_order_details(order_id)
            order = data["order"]
            items = data["items"]

            if order is None:
                messagebox.showerror("Error", "Order not found.")
                return

            self.title_label.config(text=f"Order #{order['OrderID']} Details")

            card_number = str(order.get("PaymentCardNumber") or "")
            last_four = card_number[-4:] if len(card_number) >= 4 else ""

            payment_text = "Not selected"

            if order.get("PaymentCardName"):
                payment_text = f'{order["PaymentCardName"]} ****{last_four}'

            self.info_label.config(
                text=(
                    f"Restaurant: {order['RestaurantName']}\n"
                    f"Customer: {order['CustomerName']}\n"
                    f"Driver: {order.get('DriverName') or 'Not assigned'}\n"
                    f"Payment: {payment_text}\n"
                    f"Date: {order['CreatedAt']}\n"
                    f"Status: {order['Status']}\n"
                    f"Total: ${order['TotalCost']}"
                )
            )

            for item in items:
                subtotal = item["Cost"] * item["Quantity"]

                self.items_table.insert(
                    "",
                    "end",
                    values=(
                        item["Name"],
                        f'${item["Cost"]}',
                        item["Quantity"],
                        f'${subtotal}'
                    )
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def go_back(self) -> None:
        back_page = getattr(
            self.controller,
            "previous_order_history_page",
            "CustomerOrderHistoryPage"
        )
        self.controller.show_frame(back_page)
