from tkinter import messagebox
from pages.order_history_frame import OrderHistoryFrame
from services.db import get_customer_order_history


class CustomerOrderHistoryPage(OrderHistoryFrame):

    abstract_page = False

    def __init__(self, parent, controller) -> None:
        super().__init__(
            parent,
            controller,
            back_page="CustomerHomePage"
        )

    def on_show(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            self.load_orders([])
            return

        try:
            orders = get_customer_order_history(customer["CustomerID"])
            self.load_orders(orders)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
