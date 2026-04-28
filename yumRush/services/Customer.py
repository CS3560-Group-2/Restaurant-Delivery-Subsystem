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

class Customer(User):
  """
  represents a customer placing delivery orders
  extends User class with functionality such as payment methods and order interaction
  """

  def __init__(self, accountID: int, address: Address, name: str):
    super().__init__(accountID, name)

    # customer's delivery address
    self.address = address

    # list of payment methods
    self.payment_methods: List[PaymentMethod] = []

  def sign_up(self) -> bool:
    """
    insterts customer into DB
    """
    super().sign_up("Customer")
  
    cur.execute("""INSERT INTO Customers (CustomerID, Address) VALUES %s, %s)""", (self.accountID, str(self.address)))
    con.commit()
    
    return True


  def add_payment_method(self, payment_method: PaymentMethod) -> None:
    """
    adds a new payment method to customer account
    """
    self.payment_methods.append(payment_method)
    cur.execute("""INSERT INTO PaymentMethods (PaymentID, CardNumber, CardType, CustomerID)) VALUES (%s, %s, %s, %s)""", (payment_method.payment_id, payment_method.card_number, payment_method.card_type, self.accountID))
    con.commit()

  def remove_payment_method(self, payment_method_id: int) -> bool:
    """
    remove a payment method from list
    returns True if removal was successful, False otherwise
    """
    for pm in self.payment_methods:
      if pm.payment_id == payment_method_id:
        self.payment_methods.remove(pm)
        cur.execute("""DELETE FROM PaymentMethods WHERE PaymentID = %s""", (payment_method_id, self.accountID))
        con.commit()
        return True
    return False

  def update_delivery_instructions(self, order, instructions: str) -> bool:
    """
    allows customer to modify delivery instructions
    only works if the order has not progressed too far
    """
    if order.status in ["placed", "preparing"]:
      order.delivery_instructions = instructions
      cur.execute("""UPDATE Orders SET DeliveryInstructions = %s WHERE OrderID = %s""", (instructions, order.order_id))
      con.commit()
      return True
    return False
