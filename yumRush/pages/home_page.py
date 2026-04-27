from tkinter import ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        title = ttk.Label(self, text="YumRush",font=("Helvetica", 36, "bold"),)
        #column centering 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        title.grid(column=1, row=0)

        #Driver Options
        ttk.Label(self, text="Driver Sign in").grid(column=0, row=4, padx=10, pady=10)
        ttk.Button(self, text="Sign in", command=lambda: controller.show_frame("DriverSignInPage")).grid(column=0, row=5, pady=10)
        ttk.Button(self, text="Sign up", command=lambda: controller.show_frame("DriverSignUpPage")).grid(column=0, row=7, pady=10) 

        #Customer Options
        ttk.Label(self, text="Customer Sign in").grid(column=1, row=4, padx=10, pady=10)
        ttk.Button(self, text="Sign in", command=lambda: controller.show_frame("CustomerSignInPage")).grid(column=1, row=5, pady=10)
        ttk.Button(self, text="Sign up", command=lambda: controller.show_frame("CustomerSignUpPage")).grid(column=1, row=7, pady=10) 

        #Restaurant Options 
        ttk.Label(self, text="Restaurant Sign in").grid(column=2, row=4, padx=10, pady=10)
        ttk.Button(self, text="Sign in", command=lambda: controller.show_frame("RestaurantSignInPage")).grid(column=2, row=5, pady=10)
        ttk.Button(self, text="Sign up", command=lambda: controller.show_frame("RestaurantSignUpPage")).grid(column=2, row=7, pady=10) 
