class DeliveryTicket:
    """
    Represents a delivery ticket in the system.
    This class is used to monitor whether a ticket is overdue.
    """

    def __init__(self, ticket_id: int, status: str, max_delivery_time: int):
        self.ticket_id = ticket_id
        self.status = status
        self.max_delivery_time = max_delivery_time
        self.overdue = False

    def check_overdue(self, elapsed_time: int) -> bool:
        """
        Check whether the ticket has exceeded the maximum delivery time.
        Returns True if overdue, otherwise False.
        """
        pass

    def mark_overdue(self) -> None:
        """
        Mark the ticket as overdue.
        """
        pass

    def close_ticket(self) -> None:
        """
        Close the delivery ticket.
        """
        pass


class OverdueTicketHandler:
    """
    Handles use case: Ticket is Not Closed Within Maximum Delivery Time.
    """

    def __init__(self, handler_id: int, name: str):
        self.handler_id = handler_id
        self.name = name

    def handle_overdue_ticket(self, ticket: DeliveryTicket) -> None:
        """
        Handle a ticket that is not closed within maximum delivery time.
        """
        pass

    def send_overdue_notification(self, ticket: DeliveryTicket) -> None:
        """
        Send a notification when a ticket becomes overdue.
        """
        pass