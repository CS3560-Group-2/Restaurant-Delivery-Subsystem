class Delivery:
    def __init__(self, delivery_id: int, status: str):
        self.delivery_id = delivery_id
        self.status = status

    # Confirm delivery
    def confirm_delivery(self):
        """
        Confirms the delivery of the order.
        """
        self.status = "Delivered"