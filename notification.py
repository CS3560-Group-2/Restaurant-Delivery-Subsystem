class Notification:
    def __init__(self, notification_id: int, message: str):
        self.notification_id = notification_id
        self.message = message

    # Send notification to customer
    def send(self, customer):
        """
        Sends notification to a customer.
        :param customer: Customer object
        """
        customer.receive_notification(self)