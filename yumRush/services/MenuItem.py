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

class MenuItem:
    """
    represents a menu item offered by a restaurant
    """

    def __init__(self, item_id: int, name: str, price: float, restaurant_id: int):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.restaurant_id = restaurant_id

    def save_to_db(self) -> None:
        """
        inserts menu item into database
        """
        cur.execute("""INSERT INTO MenuItems (ItemID, Name, Price, RestaurantID) VALUES (%s, %s, %s, %s)""", (self.item_id, self.name, self.price, self.restaurant_id))
        con.commit()

    def update_price(self, new_price: float) -> None:
        """
        updates price in both memory and database
        """
        self.price = new_price

        cur.execute("""UPDATE MenuItems SET Price = %s WHERE ItemID = %s""", (new_price, self.item_id))
        con.commit()

    def delete_from_db(self) -> None:
        """
        removes item from database
        """
        cur.execute("""DELETE FROM MenuItems WHERE ItemID = %s""", (self.item_id,))
        con.commit() 
