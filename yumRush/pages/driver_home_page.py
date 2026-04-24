from tkinter import ttk


class DriverHomePage(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)

        statusOptions = ["unavailable", "On route", "available", "arrived"]


        ttk.Label(self, text="Driver Home Page").grid(column=0, row=2, padx=10, pady=10)
        #status dropdown
        self.grid_columnconfigure(3, weight=1)
        statusDropDown = ttk.Combobox(self, values=statusOptions)
        statusDropDown.set("Set Status")
        statusDropDown.grid(column=0, row=3, padx=10,pady=20)
        statusDisplay = ttk.Label(self, text = "unavailable")
        statusDisplay.grid(column=3, row=0, padx=10,pady=10, sticky="e")

        def confirmStatus():
            statusDisplay.config(text=f"{statusDropDown.get()}")
            
        ttk.Button(self, text = "Sign out", command=lambda: controller.show_frame("HomePage")).grid(column=0, row=5, padx=10, pady=10)
        ttk.Button(self, text = "Status Update", command=confirmStatus).grid(column=1, row=3, padx=10, pady=20)
