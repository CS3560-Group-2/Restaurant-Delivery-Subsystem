import tkinter as tk
from tkinter import ttk, messagebox
from services.db import (
    create_payment_method,
    get_payment_methods,
    delete_payment_method
)


class CustomerPaymentMethodsPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ttk.Label(
            self,
            text="Payment Methods",
            font=("Arial", 18, "bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # LEFT: add card form
        form_frame = ttk.Frame(main_frame, padding=15, relief="ridge")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(
            form_frame,
            text="Add New Card",
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        labels = [
            "Card Name",
            "Card Number",
            "Expiration Date",
            "CVV"
        ]

        self.entries = {}

        for i, label in enumerate(labels, start=1):
            ttk.Label(form_frame, text=label).grid(
                row=i,
                column=0,
                padx=10,
                pady=5,
                sticky="e"
            )

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=5,
                sticky="w"
            )

            self.entries[label] = entry

        ttk.Button(
            form_frame,
            text="Add Card",
            command=self.add_card
        ).grid(row=5, column=0, columnspan=2, pady=15)

        # RIGHT: saved cards
        cards_panel = ttk.Frame(main_frame, padding=15, relief="ridge")
        cards_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ttk.Label(
            cards_panel,
            text="Saved Cards",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(cards_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            cards_panel,
            orient="vertical",
            command=canvas.yview
        )

        self.scrollable_frame = ttk.Frame(canvas)
        self.canvas_window = canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(self.canvas_window, width=e.width)
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Back",
            command=lambda: controller.show_frame("CustomerHomePage")
        ).pack(side="left")

    def on_show(self) -> None:
        self.load_cards()

    def add_card(self) -> None:
        customer = self.controller.current_customer

        if customer is None:
            messagebox.showerror("Error", "No customer is signed in.")
            return

        card_name = self.entries["Card Name"].get().strip()
        card_number = self.entries["Card Number"].get().strip()
        expiration_date = self.entries["Expiration Date"].get().strip()
        cvv = self.entries["CVV"].get().strip()

        if not all([card_name, card_number, expiration_date, cvv]):
            messagebox.showerror("Error", "Please fill out all card fields.")
            return

        try:
            create_payment_method(
                customer["CustomerID"],
                card_name,
                card_number,
                expiration_date,
                cvv
            )

            for entry in self.entries.values():
                entry.delete(0, tk.END)

            self.load_cards()
            messagebox.showinfo("Success", "Card added successfully.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_cards(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        customer = self.controller.current_customer

        if customer is None:
            ttk.Label(
                self.scrollable_frame,
                text="No customer signed in."
            ).pack(anchor="w", padx=10, pady=10)
            return

        try:
            cards = get_payment_methods(customer["CustomerID"])

            if not cards:
                ttk.Label(
                    self.scrollable_frame,
                    text="No saved cards yet."
                ).pack(anchor="w", padx=10, pady=10)
                return

            for card in cards:
                self.create_card_display(card)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def create_card_display(self, card: dict) -> None:
        card_frame = ttk.Frame(
            self.scrollable_frame,
            padding=12,
            relief="ridge",
            borderwidth=1
        )
        card_frame.pack(fill="x", expand=True, padx=10, pady=8)

        card_frame.grid_columnconfigure(0, weight=1)

        card_number = str(card.get("CardNumber", ""))
        last_four = card_number[-4:] if len(card_number) >= 4 else card_number

        ttk.Label(
            card_frame,
            text=card.get("CardName", "Unnamed Card"),
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            card_frame,
            text=f"Card: **** **** **** {last_four}"
        ).grid(row=1, column=0, sticky="w", pady=2)

        ttk.Label(
            card_frame,
            text=f"Expires: {card.get('ExpirationDate', '')}"
        ).grid(row=2, column=0, sticky="w", pady=2)

        ttk.Button(
            card_frame,
            text="Delete",
            command=lambda c=card: self.delete_card(c)
        ).grid(row=0, column=1, rowspan=3, padx=10, sticky="e")

    def delete_card(self, card: dict) -> None:
        confirm = messagebox.askyesno(
            "Delete Card",
            "Are you sure you want to delete this payment method?"
        )

        if not confirm:
            return

        try:
            delete_payment_method(card["PaymentMethodID"])
            self.load_cards()
            messagebox.showinfo("Success", "Card deleted.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
