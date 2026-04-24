from typing import List, Optional

class Driver(User):
    """
    represents a delivery driver in the system
    handles order pickup, delivery execution, and real-life location updates
    """
    
    def __init__(self, accountID: int, licensePlate: str, name: str, location: Address):
        super().__init__(accountID, name)

        # vehicle identifier
        self.licensePlate = licensePlate

        # current geographic location of the driver
        self.location = location

        # driver availability status (available, assigned, delivering)
        self.status = "available"

        # the order currently assigned to the driver (if any)
        self.current_order = None

    def assign_order(self, order) -> bool:
        """
        assigns an order to the driver if available
        updates driver state
        """
        if self.status == "available":
            self.current_oder = order
            self.status = "assigned"
        return False

    def update_location(self, location: Address) -> None:
        """
        updates driver's current location
        """
        self.location = location
    
    def complete_delivery(self) -> None:
        """
        finalize delivery of the current order
        resets driver availability and updates order status
        """
        if self.current_order:
            self.current_order.status = "delivered"
            self.current_order = None
            self.status = "available"
            return True
        return False
