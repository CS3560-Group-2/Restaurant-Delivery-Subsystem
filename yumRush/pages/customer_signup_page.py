from tkinter import ttk

class CustomerSignUpPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        ttk.Label(self, text="Customer Sign Up").grid(column=0, row=2, padx=10, pady=10)
        ttk.Label(self, text= "Customer Name").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=3, padx=10, pady=5)
        ttk.Label(self, text= "Username").grid(column=0, row=4, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=4, padx=10, pady=5)
        ttk.Label(self, text="Address: ").grid(column=0, row=5, padx=10, pady=5)
        ttk.Label(self, text="Street ").grid(column=0, row=6, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=6, padx=10, pady=5)
        ttk.Label(self, text="City ").grid(column=0, row=7, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=7, padx=10, pady=5)
        ttk.Label(self, text="State ").grid(column=0, row=8, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=8, padx=10, pady=5)
        ttk.Label(self, text="Zip Code ").grid(column=0, row=9, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=9, padx=10, pady=5)
        ttk.Label(self, text="Country ").grid(column=0, row=10, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=10, padx=10, pady=5)
        ttk.Button(self, text="Next", command=lambda: controller.show_frame("PaymentMethodPage")).grid(column=1, row=11, padx=10, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage")).grid(column=0, row=11, padx=10, pady=10)


