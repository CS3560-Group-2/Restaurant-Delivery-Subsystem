from tkinter import ttk, messagebox
from services.db import get_order_details, create_restaurant_review, create_driver_review


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

        review_frame = ttk.LabelFrame(self, text="Leave a Review", padding=10)
        review_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        ttk.Label(review_frame, text="Restaurant Rating:").grid(row=0, column=0, sticky="w")
        self.restaurant_rating = ttk.Combobox(review_frame, values=[1, 2, 3, 4, 5], state="readonly")
        self.restaurant_rating.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(review_frame, text="Restaurant Review:").grid(row=1, column=0, sticky="w")
        self.restaurant_review_text = ttk.Entry(review_frame, width=50)
        self.restaurant_review_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(review_frame, text="Driver Rating:").grid(row=2, column=0, sticky="w")
        self.driver_rating = ttk.Combobox(review_frame, values=[1, 2, 3, 4, 5], state="readonly")
        self.driver_rating.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(review_frame, text="Driver Review:").grid(row=3, column=0, sticky="w")
        self.driver_review_text = ttk.Entry(review_frame, width=50)
        self.driver_review_text.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(
            review_frame,
            text="Submit Reviews",
            command=self.submit_reviews
        ).grid(row=4, column=1, sticky="e", pady=10)

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
            self.current_order = order

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

    def submit_reviews(self) -> None:
        if not hasattr(self, "current_order") or self.current_order is None:
            messagebox.showerror("Error", "No order selected.")
            return

        order = self.current_order
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            return

        if order["Status"] != "Delivered":
            messagebox.showerror("Error", "You can only review delivered orders.")
            return

        if order.get("DriverID") is None:
            messagebox.showerror("Error", "This order does not have a driver assigned.")
            return

        restaurant_rating = self.restaurant_rating.get()
        driver_rating = self.driver_rating.get()

        if not restaurant_rating or not driver_rating:
            messagebox.showerror("Error", "Please select both ratings.")
            return

        try:
            create_restaurant_review(
                order["OrderID"],
                customer["CustomerID"],
                order["RestaurantID"],
                int(restaurant_rating),
                self.restaurant_review_text.get().strip()
            )

            create_driver_review(
                order["OrderID"],
                customer["CustomerID"],
                order["DriverID"],
                int(driver_rating),
                self.driver_review_text.get().strip()
            )

            messagebox.showinfo("Success", "Reviews submitted successfully.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))


