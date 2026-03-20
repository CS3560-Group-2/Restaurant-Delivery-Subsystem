class Restaurant:
    def __init__(self, restaurant_id: int, name: str, location: str):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location

    # Restaurant cancels order
    def cancel_order(self, order):
        """
        Cancels an order from the restaurant side.
        :param order: Order object
        :return: Boolean indicating success
        """
        if order.is_cancellable():
            order.update_status("Cancelled")
            return True
        return False