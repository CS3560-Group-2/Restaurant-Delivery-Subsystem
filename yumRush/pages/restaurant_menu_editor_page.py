from tkinter import ttk, messagebox
from services.db import add_menu_item, update_menu_item, delete_menu_item, get_menu_items


class MenuEditor(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        table_frame = ttk.Frame(self)
        table_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Menu Entry").grid(column=0, row=1, padx=10, pady=10)

        columns = ("name", "price")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.table.heading("name", text="Name")
        self.table.heading("price", text="Price")
        self.table.column("name", width=200)
        self.table.column("price", width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(column=0, row=0, sticky="nsew")
        scrollbar.grid(column=1, row=0, sticky="ns")

        self.table.bind("<<TreeviewSelect>>", self.load_selected_row)

        form = ttk.Frame(self)
        form.grid(column=0, row=2, padx=10, pady=10, sticky="w")

        ttk.Label(form, text="Name").grid(column=0, row=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(form, width=20)
        self.name_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(form, text="Price").grid(column=2, row=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(form, width=20)
        self.price_entry.grid(column=3, row=0, padx=10, pady=10)

        ttk.Button(form, text="Add Item", command=self.add_item).grid(column=4, row=0, padx=5, pady=10)
        ttk.Button(form, text="Update Item", command=self.update_item).grid(column=5, row=0, padx=5, pady=10)
        ttk.Button(form, text="Delete Item", command=self.delete_item).grid(column=6, row=0, padx=5, pady=10)
        ttk.Button(form, text="Submit", command=self.submit_menu).grid(column=7, row=0, padx=5, pady=10)

        #self.refresh_table()

    def get_restaurant_id(self):
        restaurant = getattr(self.controller, "current_restaurant", None)

        if restaurant is None:
            messagebox.showerror("Error", "No restaurant is signed in.")
            return None

        return restaurant["RestaurantID"]

    def refresh_table(self):
        restaurant_id = self.get_restaurant_id()
        if restaurant_id is None:
            return

        for row in self.table.get_children():
            self.table.delete(row)

        for menu_item_id, name, price in get_menu_items(restaurant_id):
            self.table.insert(
                "",
                "end",
                iid=str(menu_item_id),
                values=(name, price)
            )

    def add_item(self) -> None:
        restaurant_id = self.get_restaurant_id()
        if restaurant_id is None:
            return

        name = self.name_entry.get().strip()
        price_text = self.price_entry.get().strip()

        if not name or not price_text:
            messagebox.showerror("Error", "Please enter a name and price.")
            return

        try:
            price = int(price_text)
            add_menu_item(restaurant_id, name, price)
            self.refresh_table()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Price must be a whole number.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_selected_row(self, event=None) -> None:
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0], "values")

        self.clear_entries()
        self.name_entry.insert(0, values[0])
        self.price_entry.insert(0, values[1])

    def update_item(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update.")
            return

        name = self.name_entry.get().strip()
        price_text = self.price_entry.get().strip()

        if not name or not price_text:
            messagebox.showerror("Error", "Please enter a name and price.")
            return

        try:
            menu_item_id = int(selected[0])
            price = int(price_text)

            update_menu_item(menu_item_id, name, price)
            self.refresh_table()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Price must be a whole number.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_item(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        try:
            menu_item_id = int(selected[0])
            delete_menu_item(menu_item_id)
            self.refresh_table()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def submit_menu(self):
        self.refresh_table()
        self.controller.show_frame("RestaurantDashboardPage")

    def clear_entries(self) -> None:
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")

    def on_show(self):
        self.refresh_table()

