class Driver:
    """
    Represents a driver account creation process.
    """

    def __init__(self, name: str, license_plate: str):
        self.name = name
        self.license_plate = license_plate

    def sign_up(self) -> None:
        """
        Use case: Driver Signs Up
        Create a new driver account in the system.
        """
        pass