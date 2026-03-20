from typing import List, Optional

class DeliveryService:
    def __init__(self):
        self.orders: List[Order] = []
        self.drivers: List[Driver] = []

    # assign delivery to a driver
    def assign_driver_to_order(self, order_id: int) -> Optional[Driver]:
        """
        assigns an available driver to an order
        returns assigned Driver or None if unavailable
        """
        order = self._find_order(order_id)
        if not order or order.status != "ready":
            return None

        for driver in self.drivers:
            if driver.is_available:
                if driver.assign_order(order):
                    order.assigned_driver = driver
                    order.status = "out_for_delivery"
                    return driver

        return None  # No available drivers

    def _find_order(self, order_id: int) -> Optional[Order]:
        """
        helper method to find an order by ID
        """
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def add_driver(self, driver: Driver) -> None:
        self.drivers.append(driver)

    def add_order(self, order: Order) -> None:
        self.orders.append(order)
