#for loading in the different pages/frames
import importlib
import inspect
import pkgutil
import pages
#tkinter setup
import tkinter as tk
from tkinter import ttk


class YumRushApp(tk.Tk):
    #constructor
    def __init__(self) -> None:
        super().__init__()
        self.title("YumRush")
        self.geometry("800x600")

        # container/Frame attribute definition
        container = ttk.Frame(self, padding=(8,8,8,8))
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, ttk.Frame] = {}

        #load the frames from /pages
        for PageClass in self.load_pages():
          frame = PageClass(container, self)
          self.frames[PageClass.__name__] = frame
          frame.grid(row=0, column=0, sticky="nsew")

        #show the home page when app os launched
        self.show_frame("HomePage")

    def load_pages(self) -> list[type[ttk.Frame]]:
        page_classes = []

        for _, module_name, _ in pkgutil.iter_modules(pages.__path__):
            module = importlib.import_module(f"pages.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, ttk.Frame) and obj is not ttk.Frame:
                    page_classes.append(obj)

        return page_classes

    def show_frame(self, page_name: str) -> None:
        frame = self.frames[page_name]
        frame.tkraise()
