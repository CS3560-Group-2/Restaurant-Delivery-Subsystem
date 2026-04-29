from typing import Optional, List
import mysql.connector

# database connection setup
con = mysql.connector.connect(
  user = 'root',
  host = 'localhost',
  database = 'food_delivery', # placeholder name
  passwd = 'password' # placeholder password
)

cur = con.cursor()

class Driver(User):
    """
    represents a delivery driver in the system
    handles order pickup, delivery execution, and real-life location updates
    """
    
    def __init__(self, accountID: int, licensePlate: str):
        super().__init__(accountID)

        # vehicle identifier
        self.license_plate = licensePlate

        # driver availability status (available, assigned, delivering)
        self.status = "available"

        # the order currently assigned to the driver (if any)
        self.current_order = None
    
    def sign_up(self) -> bool:
       """
       inserts driver into DB
       """
       super().sign_up("Driver")

       cur.execute("""INSERT INTO Drivers (DriverID, LicensePlate, Location, Status) VALUES (%s, %s, %s)""", (self.accountID, self.license_plate, self.status))
       con.commit()

       return True

    def assign_order(self, order) -> bool:
        """
        assigns an order to the driver if available
        updates driver state
        """
        if self.status == "available":
            self.current_order = order
            self.status = "assigned"
            cur.execute("""UPDATE Orders SET DriverID = %s, Status = %s WHERE OrderID = %s""", (self.accountID, "delivering", order.order_id))
            con.commit()
            return True
        return False
    
    def complete_delivery(self) -> None:
        """
        finalize delivery of the current order
        resets driver availability and updates order status
        """
        if self.current_order:
            self.current_order.status = "delivered"
            cur.execute("""UPDATE Orders SET Status = %s WHERE OrderID = %s""", ("delivered", self.current_order.order_id))
            con.commit()
            self.current_order = None
            self.status = "available"
            return True
        return False
