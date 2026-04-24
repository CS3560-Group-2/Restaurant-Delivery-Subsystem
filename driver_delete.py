class Driver:
    """
    Represents a driver account in the system.
    """

    def __init__(self, driver_id: int, name: str, status: str):
        self.driver_id = driver_id
        self.name = name
        self.status = status

    def delete_account(self) -> None:
        """
        Use case: Driver Deletes Account
        Remove or deactivate the driver account from the system.
        """
        pass