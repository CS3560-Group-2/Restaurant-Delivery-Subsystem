# for loading in the different pages/frames
import importlib
import inspect
import pkgutil
import pages

# tkinterbootstrap setup
import ttkbootstrap as ttk


class YumRushApp(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="superhero")

        self.title("YumRush")
        self.geometry("1200x900")

        self.current_driver = None
        self.current_customer = None
        self.current_restaurant = None
        self.current_order_restaurant = None
        self.current_order_id = None
        self.previous_order_history_page = "CustomerOrderHistoryPage"

        container = ttk.Frame(self, padding=(8, 8, 8, 8))
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, ttk.Frame] = {}

        for PageClass in self.load_pages():
            frame = PageClass(container, self)
            self.frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def load_pages(self) -> list[type[ttk.Frame]]:
        page_classes = []

        for _, module_name, _ in pkgutil.iter_modules(pages.__path__):
            module = importlib.import_module(f"pages.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, ttk.Frame)
                    and obj is not ttk.Frame
                    and not getattr(obj, "abstract_page", False)
                ):
                    page_classes.append(obj)

        return page_classes 

    def show_frame(self, page_name: str) -> None:
        frame = self.frames[page_name]

        if hasattr(frame, "on_show"):
            frame.on_show()

        frame.tkraise()

    
