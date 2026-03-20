from typing import List, Optional

class Driver:
    def __init__(self, driver_id: int, name: str):
        self.driver_id: int = driver_id
        self.name: str = name
        self.is_available: bool = True
        self.current_order: Optional[Order] = None

    def assign_order(self, order: Order) -> bool:
        """
        assigns an order to the driver if available
        """
        if self.is_available:
            self.current_order = order
            self.is_available = False
            return True
        return False

    def complete_delivery(self) -> None:
        """
        marks delivery complete and frees driver
        """
        self.current_order = None
        self.is_available = True
