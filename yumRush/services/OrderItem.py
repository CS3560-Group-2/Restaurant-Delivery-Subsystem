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

class OrderItem:
    """
    represents a specific item within an order
    """

    def __init__(self, order_id: int, menu_item: MenuItem, quantity: int):
        self.order_id = order_id
        self.menu_item = menu_item
        self.quantity = quantity

    def save_to_db(self) -> None:
        """
        inserts order item into database
        """
        cur.execute("""INSERT INTO OrderItems (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)""", (self.order_id, self.menu_item.item_id, self.quantity))
        con.commit()

    def update_quantity(self, new_quantity: int) -> None:
        """
        updates quantity in database
        """
        self.quantity = new_quantity

        cur.execute("""UPDATE OrderItems SET Quantity = %s WHERE OrderID = %s AND ItemID = %s""", (new_quantity, self.order_id, self.menu_item.item_id))
        con.commit()

    def delete_from_db(self) -> None:
        """
        removes this item from the order
        """
        cur.execute("""DELETE FROM OrderItems WHERE OrderID = %s AND ItemID = %s""", (self.order_id, self.menu_item.item_id))
        con.commit()

    def get_total_price(self) -> float:
        """
        calculates subtotal for this item
        """
        return self.menu_item.price * self.quantity
