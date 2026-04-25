from tkinter import ttk

class PaymentMethodPage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        ttk.Label(self, text="Payment Method ").grid(column=0, row=2, padx=10, pady=10)
        ttk.Label(self, text= "Card Number").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self).grid(column=1, row=3, padx=10, pady=5)
        
        ttk.Button(self, text="Next", command=lambda: controller.show_frame("CustomerHomePage")).grid(column=1, row=11, padx=10, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("CustomerSignUpPage")).grid(column=0, row=11, padx=10, pady=10)


