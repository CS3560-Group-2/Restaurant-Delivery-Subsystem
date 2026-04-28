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

class Order:
    """
    represents a customer's order in the delivery system
    handles item management, pricing, and status transitions
    """

    def __init__(self, order_id: int, customer: Customer, restaurant: Restaurant):
        self.order_id = order_id
        self.customer = customer
        self.restaurant = restaurant

        # list of items in the order
        self.items: List[MenuItem] = []

        # current order status (placed, preparing, ready, delivering, delivered, cancelled)
        self.status = "placed"

        # assigned driver
        self.driver: Optional[Driver] = None

        # delivery instructions from customer
        self.delivery_instructions = ""

        # total price of order
        self.total_price = 0.0

    def save_to_db(self) -> None:
        """
        inserts new order into database
        """

        cur.execute("""INSERT INTO Orders (OrderID, CustomerID, RestaurantID, Status, TotalPrice, Intructions) VALUES (%s, %s, %s, %s, %s, %s)""", (
           self.order_id,
           self.customer.accountID,
           self.restaurant.accountID,
           self.status,
           self.total_price,
           self.delivery_instructions
        ))
        con.commit()

    def add_item(self, item: MenuItem) -> None:
        """
        adds an item to the order and updates total price
        """
        self.items.append(item)
        self.total_price += item.price

        cur.execute("""INSERT INTO OrderItems (OrderID, ItemID) VALUES (%s, %s)""", (self.order_id, item.item_id))
        cur.execute("""UPDATE ORDERS SET TotalPrice = %s WHERE ORDERID = %s""", (self.total_price, self.order_id))
        con.commit()

    def remove_item(self, item_id: int) -> bool:
        """
        removes an item from the order by ID
        updates total price accordingly
        """
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                self.total_price -= item.price
                cur.execute("""DELETE FROKM OrderItems WHERE OrderID = %s AND ItemID = %s""", (self.order_id, item_id))
                cur.execute("""UPDATE ORDERS SET TOotalPrice = %s WHERE OrderID = %s""", (self.total_price, self.order_id))
                con.commit()
                return True
        return False

    def calculate_total(self) -> float:
        """
        recalculates total price (useful for validation)
        """
        self.total_price = sum(item.price for item in self.items)
        return self.total_price

    def assign_driver(self, driver: Driver) -> bool:
        """
        assigns a driver if order is ready
        """
        if self.status == "ready" and driver.status == "available":
            self.driver = driver
            driver.assign_order(self)
            self.status = "delivering"
            cur.execute("""UPDATE Orders SET DriverID = %s, Status = %s WHERE OrderID = %s""", (
               driver.accountID,
               self.status,
               self.order_id
            ))
            con.commit()
            return True
        return False

    def update_status(self, new_status: str) -> None:
        """
        updates order status in databse
        """

        self.status = new_status

        cur.execute("""UPDATE Orders SET Status = %s WHERE OrderID = %s""", (new_status, self.order_id))
        con.commit()

    # old update_status method, not currently in use
    '''
    def update_status(self, new_status: str) -> bool:
        """
        safely updates order status with simple validation
        """
        valid_transitions = {
            "placed": ["preparing", "cancelled"],
            "preparing": ["ready", "cancelled"],
            "ready": ["delivering"],
            "delivering": ["delivered"],
            "delivered": [],
            "cancelled": []
        }

        if new_status in valid_transitions[self.status]:
            self.status = new_status
            return True
        return False
    '''

    def cancel_order(self) -> bool:
        """
        cancels the order if it hasn't been delivered
        """
        if self.status in ["placed", "preparing"]:
            self.status = "cancelled"
            cur.execute("""UPDATE Orders SET STATUS = %s WHERE ORDERID = %s""", ("cancelled", self.order_id))
            con.commit()
            return True
        return False
