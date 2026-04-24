from tkinter import ttk


class RestaurantHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        ttk.Label(self, text = "Restaurant Home Page").grid(column=0, row=2, padx=10, pady=10)
        ttk.Button(self, text = "Sign out", command=lambda: controller.show_frame("HomePage")).grid(column=0, row=5, padx=10, pady=10)
