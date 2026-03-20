class Customer:
    def __init__(self, customer_id: int, name: str, phone: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    # Cancel an order
    def cancel_order(self, order):
        """
        Cancels the given order if possible.
        :param order: Order object
        :return: Boolean indicating success
        """
        if order.is_cancellable():
            order.update_status("Cancelled")
            return True
        return False

    # Receive notification
    def receive_notification(self, notification):
        """
        Receives a notification.
        :param notification: Notification object
        """
        print(f"Notification for {self.name}: {notification.message}")