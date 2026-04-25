from tkinter import ttk


class MenuInitialPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        # ===== TABLE =====
        table_frame = ttk.Frame(self)
        table_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Menu Entry").grid(column=0, row=1, padx=10, pady=10)

        columns = ("name", "price")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.table.heading("name", text="Name")
        self.table.heading("price", text="Price")

        self.table.column("name", width=200)
        self.table.column("price", width=200)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(column=0, row=0, sticky="nsew")
        scrollbar.grid(column=1, row=0, sticky="ns")

        # Load selected row into entry boxes
        self.table.bind("<<TreeviewSelect>>", self.load_selected_row)

        # ===== FORM =====
        form = ttk.Frame(self)
        form.grid(column=0, row=2, padx=10, pady=10, sticky="w")

        ttk.Label(form, text="Name").grid(column=0, row=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(form, width=20)
        self.name_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(form, text="Price").grid(column=2, row=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(form, width=20)
        self.price_entry.grid(column=3, row=0, padx=10, pady=10)

        ttk.Button(
            form,
            text="Add Item",
            command=self.add_item
        ).grid(column=4, row=0, padx=0, pady=10)

        ttk.Button(
            form,
            text="Update Item",
            command=self.update_item
        ).grid(column=5, row=0, padx=0, pady=10)

        ttk.Button(
            form,
            text="Delete Item",
            command=self.delete_item
        ).grid(column=6, row=0, padx=0, pady=10)
        ttk.Button(
            form,
            text="Submit",
            command=lambda: controller.show_frame("RestaurantDashboardPage")
        ).grid(column=7, row=0, padx=0, pady=10)

    def add_item(self) -> None:
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not price:
            return

        self.table.insert("", "end", values=(name, price))
        self.clear_entries()

    def load_selected_row(self, event=None) -> None:
        selected = self.table.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.table.item(item_id, "values")

        self.clear_entries()
        self.name_entry.insert(0, values[0])
        self.price_entry.insert(0, values[1])

    def update_item(self) -> None:
        selected = self.table.selection()
        if not selected:
            return

        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not price:
            return

        item_id = selected[0]
        self.table.item(item_id, values=(name, price))
        self.clear_entries()

    def delete_item(self) -> None:
        selected = self.table.selection()
        if not selected:
            return

        item_id = selected[0]
        self.table.delete(item_id)
        self.clear_entries()

    def clear_entries(self) -> None:
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
