from tkinter import ttk


class RestaurantDashboardPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Restaurant Dashboard").grid(
            column=0, row=0, columnspan=2, padx=10, pady=20
        )

        ttk.Button(
            self,
            text="Edit Restaurant Info",
            command=lambda: self.controller.show_frame("RestaurantEditAccountPage")
        ).grid(column=0, row=1, padx=10, pady=10)

        ttk.Button(
            self,
            text="Edit Menu",
            command=lambda: self.controller.show_frame("MenuEditor")
        ).grid(column=0, row=2, padx=10, pady=10)

        ttk.Button(
            self,
            text="Sign Out",
            command=self.sign_out
        ).grid(column=0, row=3, padx=10, pady=10)

    def sign_out(self):
        self.controller.current_restaurant = None
        self.controller.show_frame("HomePage")
