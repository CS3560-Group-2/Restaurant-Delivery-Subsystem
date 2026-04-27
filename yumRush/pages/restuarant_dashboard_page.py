from tkinter import ttk


class RestaurantDashboardPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # =========================
        # TITLE
        # =========================
        title = ttk.Label(self, text="Restaurant Dashboard")
        title.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        # =========================
        # PROFILE SECTION
        # =========================
        profile_frame = ttk.LabelFrame(self, text="Restaurant Info", padding=15)
        profile_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        profile_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(profile_frame, text="Restaurant Name").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.restaurant_name_entry = ttk.Entry(profile_frame, width=35)
        self.restaurant_name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(profile_frame, text="Username").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.username_entry = ttk.Entry(profile_frame, width=35)
        self.username_entry.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(profile_frame, text="Address").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.address_entry = ttk.Entry(profile_frame, width=35)
        self.address_entry.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        ttk.Button(
            profile_frame,
            text="Save Info",
            command=self.save_restaurant_info
        ).grid(row=3, column=1, padx=10, pady=12, sticky="e")

        self.info_status_label = ttk.Label(profile_frame, text="")
        self.info_status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # =========================
        # MENU SECTION
        # =========================
        menu_frame = ttk.LabelFrame(self, text="Menu Manager", padding=15)
        menu_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        menu_frame.grid_rowconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(0, weight=1)

        columns = ("name", "price")
        self.menu_table = ttk.Treeview(
            menu_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.menu_table.heading("name", text="Item Name")
        self.menu_table.heading("price", text="Price")

        self.menu_table.column("name", width=220)
        self.menu_table.column("price", width=140)

        menu_scrollbar = ttk.Scrollbar(
            menu_frame,
            orient="vertical",
            command=self.menu_table.yview
        )
        self.menu_table.configure(yscrollcommand=menu_scrollbar.set)

        self.menu_table.grid(row=0, column=0, sticky="nsew")
        menu_scrollbar.grid(row=0, column=1, sticky="ns")

        self.menu_table.bind("<<TreeviewSelect>>", self.load_selected_menu_item)

        # =========================
        # MENU FORM
        # =========================
        form = ttk.Frame(menu_frame)
        form.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="w")

        ttk.Label(form, text="Item Name").grid(row=0, column=0, padx=10, pady=8)
        self.menu_name_entry = ttk.Entry(form, width=25)
        self.menu_name_entry.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(form, text="Price").grid(row=0, column=2, padx=10, pady=8)
        self.menu_price_entry = ttk.Entry(form, width=20)
        self.menu_price_entry.grid(row=0, column=3, padx=10, pady=8)

        ttk.Button(
            form,
            text="Add Item",
            command=self.add_menu_item
        ).grid(row=0, column=4, padx=10, pady=8)

        ttk.Button(
            form,
            text="Update Item",
            command=self.update_menu_item
        ).grid(row=0, column=5, padx=10, pady=8)

        ttk.Button(
            form,
            text="Delete Item",
            command=self.delete_menu_item
        ).grid(row=0, column=6, padx=10, pady=8)

        self.menu_status_label = ttk.Label(menu_frame, text="")
        self.menu_status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # =========================
        # NAVIGATION
        # =========================
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Sign Out",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="right")

    # =========================
    # RESTAURANT INFO METHODS
    # =========================
    def save_restaurant_info(self) -> None:
        restaurant_name = self.restaurant_name_entry.get().strip()
        username = self.username_entry.get().strip()
        address = self.address_entry.get().strip()

        if not restaurant_name or not username or not address:
            self.info_status_label.config(text="Please fill out all restaurant info fields.")
            return

        # Placeholder for DB update logic
        # Example: update restaurant table in MySQL here

        self.info_status_label.config(text="Restaurant info updated successfully.")

    # =========================
    # MENU METHODS
    # =========================
    def add_menu_item(self) -> None:
        item_name = self.menu_name_entry.get().strip()
        item_price = self.menu_price_entry.get().strip()

        if not item_name or not item_price:
            self.menu_status_label.config(text="Please enter both item name and price.")
            return

        self.menu_table.insert("", "end", values=(item_name, item_price))
        self.clear_menu_entries()
        self.menu_status_label.config(text="Menu item added.")

    def load_selected_menu_item(self, event=None) -> None:
        selected = self.menu_table.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.menu_table.item(item_id, "values")

        self.clear_menu_entries()
        self.menu_name_entry.insert(0, values[0])
        self.menu_price_entry.insert(0, values[1])

    def update_menu_item(self) -> None:
        selected = self.menu_table.selection()
        if not selected:
            self.menu_status_label.config(text="Please select a menu item to update.")
            return

        item_name = self.menu_name_entry.get().strip()
        item_price = self.menu_price_entry.get().strip()

        if not item_name or not item_price:
            self.menu_status_label.config(text="Please enter both item name and price.")
            return

        item_id = selected[0]
        self.menu_table.item(item_id, values=(item_name, item_price))
        self.clear_menu_entries()
        self.menu_status_label.config(text="Menu item updated.")

    def delete_menu_item(self) -> None:
        selected = self.menu_table.selection()
        if not selected:
            self.menu_status_label.config(text="Please select a menu item to delete.")
            return

        item_id = selected[0]
        self.menu_table.delete(item_id)
        self.clear_menu_entries()
        self.menu_status_label.config(text="Menu item deleted.")

    def clear_menu_entries(self) -> None:
        self.menu_name_entry.delete(0, "end")
        self.menu_price_entry.delete(0, "end")
