class Order:
    def __init__(self, order_id: int, status: str, total_amount: float):
        self.order_id = order_id
        self.status = status
        self.total_amount = total_amount

    # Update order status
    def update_status(self, status: str):
        """
        Updates the order status.
        :param status: New status string
        """
        self.status = status

    # Check if order can be canceled
    def is_cancellable(self) -> bool:
        """
        Checks if the order can be canceled.
        :return: True if cancellable, False otherwise
        """
        return self.status != "Delivered"