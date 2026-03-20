from typing import List, Optional


class Order:
    def __init__(self, order_id: int, customer_id: int, items: List[str]):
        self.order_id: int = order_id
        self.customer_id: int = customer_id
        self.items: List[str] = items
        self.special_instructions: Optional[str] = None
        self.status: str = "placed"  # placed, preparing, ready, out_for_delivery, delivered, cancelled
        self.assigned_driver: Optional[Driver] = None

    # update existing order
    def update_instructions(self, instructions: str) -> bool:
        """
        updates special instructions for the order
        returns True if update is successful.
        """
        if self.status in ["placed", "preparing"]:
            self.special_instructions = instructions
            return True
        return False

    def update_items(self, new_items: List[str]) -> bool:
        """
        updates order items if still editable
        """
        if self.status in ["placed", "preparing"]:
            self.items = new_items
            return True
        return False
