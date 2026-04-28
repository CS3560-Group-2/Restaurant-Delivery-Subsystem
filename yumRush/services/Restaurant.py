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

class User:
  """super class representing a generic system user"""
  def __init__(self, accountID: int, name: str):
    # user account identifier
    self.accountID = accountID

    # user display name
    self.name = name

    # indicates whether account is active
    self.active = True

    # indicates whether account is logged in
    self.logged_in = False

def sign_up(self, user_type: str) -> bool:
  """
  simulates account registration
  """
  cur.execute("""
              INSERT INTO users (UserID, Type, Name, Active)) VALUES (%s, %s, %s, %s)
              """, (self.accountID, user_type, self.name, self.active))
  con.commit()
  return True

def sign_in(self) -> None:
  """
  simulates user logging in
  """
  self.logged_in = True

def sign_out(self) -> None:
  """
  simulates user logging out
  """
  self.logged_in = False

def delete_account(self) -> None:
  """
  deactivates account
  """
  self.active = False
  cur.execute("""UPDATE Users SET Active = %s WHERE UserID = %s""", (False, self.accountID))
  con.commit()

def edit_profile(self, name: Optional[str] = None) -> None:
  """
  updates user profile information
  """
  if name:
    self.name = name
    cur.execute("""UPDATE Users SET Name = %s WHERE UserID = %s""", (self.name, self.accountID))
    con.commit()

class Restaurant(User):
  """
  represents a restaurant in the delivery system
  responsible for managing menu items and updating order preparation status
  """
  def __init__(self, accountID: int, address: Address, name: str):
    super().__init__(accountID, name)

    # physical restaurant location
    self.address = address

    # list of menu items offered
    self.menu: List[MenuItem] = []

  def sign_up(self) -> bool:
     """
     inserts restaurant into DB
     """
     super().sign_up("Restaurant")

     cur.execute("""INSERT INTO Restaurants (RestaurantID, Address) VALUES (%s, %s)""", (self.accountID, str(self.address)))
     con.commit()

     return True

  def add_menu_item(self, item: MenuItem) -> None:
    """
    adds a new item to the restaurant's menu
    """
    self.menu.append(item)

    cur.execute("""INSERT INTO MenuItems (ItemID, Name, Price, RestaurantID) VALUES (%s, %s, %s, %s)""", (item.item_id, item.name, item.price, self.accountID))
    con.commit()

  def remove_menu_item(self, item_id: int) -> None:
    """
    removes a menu item from db based on ID
    """
    cur.execute("DELETE FROM MenuItems WHERE ItemID = %s", (item_id,))
    con.commit()

  # old remove_menu_item method, not currently in use
  '''
  def remove_menu_item(self, item_id: int) -> bool:
    """
    removes a menu item based on item ID
    returns true if removal is successful
    """
    for item in self.menu:
      if item.item_id == item_id:
        self.menu.remove(item)
        return True
    return False
  '''

  def mark_order_ready(self, order) -> bool:
    """
    marks order for delivery
    transitions order status from 'preparing' to ready
    signals that it can be picked up by driver
    """
    if order.status == "preparing":
      order.status = "ready"
      cur.execute("""UPDATE Orders SET Status = %s WHERE OrderID = %s""", ("ready", order.order_id))
      con.commit()
      return True
    return False
