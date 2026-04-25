from tkinter import ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        title = ttk.Label(self, text="YumRush",font=("Helvetica", 36, "bold"),)
        title.pack(pady=20)
        title.grid(column=0, row=0, padx=10, pady=20)
        ttk.Label(self, text="Driver Sign in").grid(column=0, row=2, padx=10, pady=10)
        ttk.Button(self, text="Sign in", command=lambda: controller.show_frame("DriverSignInPage")).grid(column=0, row=3, padx=10, pady=10)
        ttk.Button(self, text="Sign up", command=lambda: controller.show_frame("DriverSignUpPage")).grid(column=0, row=5, padx=10, pady=10) 
