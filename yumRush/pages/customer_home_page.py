import tkinter as tk
from tkinter import ttk


class CustomerHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        title = ttk.Label(self, text="Customer Dashboard")
        title.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        # Main container
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Canvas + scrollbar setup
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Optional mouse wheel scrolling
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        )

        # Status / selection label
        self.selected_label = ttk.Label(self, text="Selected restaurant: None")
        self.selected_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Bottom nav
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        ttk.Button(
            bottom_bar,
            text="Sign Out",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="right")

        # Example restaurant cards
        restaurants = [
            {"name": "Burger House", "cuisine": "American", "eta": "20-30 min"},
            {"name": "Pasta Corner", "cuisine": "Italian", "eta": "25-35 min"},
            {"name": "Sushi World", "cuisine": "Japanese", "eta": "30-40 min"},
            {"name": "Taco Fiesta", "cuisine": "Mexican", "eta": "15-25 min"},
            {"name": "Dragon Wok", "cuisine": "Chinese", "eta": "20-30 min"},
            {"name": "Mediterranean Grill", "cuisine": "Mediterranean", "eta": "25-35 min"},
            {"name": "Vegan Bowl", "cuisine": "Healthy", "eta": "15-20 min"},
            {"name": "Pizza Plaza", "cuisine": "Pizza", "eta": "20-30 min"},
            {"name": "Pho Station", "cuisine": "Vietnamese", "eta": "25-35 min"},
            {"name": "Curry Spot", "cuisine": "Indian", "eta": "30-40 min"},
            {"name": "Wing Hub", "cuisine": "Wings", "eta": "20-25 min"},
            {"name": "Breakfast Barn", "cuisine": "Breakfast", "eta": "15-20 min"},
        ]

        for restaurant in restaurants:
            self.create_restaurant_card(restaurant)

    def create_restaurant_card(self, restaurant: dict) -> None:
        card = ttk.Frame(self.scrollable_frame, padding=12, relief="ridge", borderwidth=1)
        card.pack(fill="x", padx=10, pady=8)

        info_frame = ttk.Frame(card)
        info_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(info_frame, text=restaurant["name"]).pack(anchor="w")
        ttk.Label(info_frame, text=f'Cuisine: {restaurant["cuisine"]}').pack(anchor="w")
        ttk.Label(info_frame, text=f'ETA: {restaurant["eta"]}').pack(anchor="w")

        ttk.Button(
            card,
            text="View",
            command=lambda r=restaurant: self.select_restaurant(r)
        ).pack(side="right", padx=10)

    def select_restaurant(self, restaurant: dict) -> None:
        self.selected_label.config(
            text=f'Selected restaurant: {restaurant["name"]}'
        )
