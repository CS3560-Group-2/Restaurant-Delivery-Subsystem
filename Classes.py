from typing import Optional, List

class User:
  """super class representing a generic system user"""
  def __init__(self, accountID: int, name: str):
    # user account identifier
    self.accountID = accountID

    # user display name
    self.name = name

    # indicates whether account is active
    self.active = True

def sign_up(self) -> bool:
  """
  simulates account registration
  """
  return True

def delete_account(self) -> None:
  """
  deactivates account
  """
  self.active = false

def edit_profile(self, name: Optional[str] = None) -> None:
  """
  updates user profile information
  """
  if name:
    self.name = name

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

  def add_menu_item(self, item: MenuItem) -> None:
    """
    adds a new item to the restaurant's menu
    """
    self.menu.append(item)

  def remove_menu_item(self, item_id: int) -> bool:
    """
    removes a menu item based on item ID
    returns true if removal is successful
    """
    for item in self.menu
      if item.item_id == item_id:
        self.menu.remove(item)
        return True
    return False

  def mark_order_ready(self, order) -> bool:
    """
    marks order for delivery
    transitions order status from 'preparing' to ready
    signals that it can be picked up by driver
    """
    if order.status == "preparing":
      order.status = "ready
      return True
    return False

class Driver(User):
    """
    represents a delivery driver in the system
    handles order pickup, delivery execution, and real-life location updates
    """
    
    def __init__(self, accountID: int, licensePlate: str, name: str, location: Address):
        super().__init__(accountID, name)

        # vehicle identifier
        self.licensePlate = licensePlate

        # current geographic location of the driver
        self.location = location

        # driver availability status (available, assigned, delivering)
        self.status = "available"

        # the order currently assigned to the driver (if any)
        self.current_order = None

    def assign_order(self, order) -> bool:
        """
        assigns an order to the driver if available
        updates driver state
        """
        if self.status == "available":
            self.current_oder = order
            self.status = "assigned"
        return False

    def update_location(self, location: Address) -> None:
        """
        updates driver's current location
        """
        self.location = location
    
    def complete_delivery(self) -> None:
        """
        finalize delivery of the current order
        resets driver availability and updates order status
        """
        if self.current_order:
            self.current_order.status = "delivered"
            self.current_order = None
            self.status = "available"
            return True
        return False

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

  def add_payment_method(self, payment_method: PaymentMethod) -> None:
    """
    adds a new payment method to customer account
    """
    self.payment_methods.append(payment_method)

  def remove_payment_method(self, payment_method_id: int) -> bool:
    """
    remove a payment method from list
    returns True if removal was successful, False otherwise
    """
    for pm in self.payment_methods:
      if pm.payment_id == payment_method_id:
        self.payment_methods.remove(pm)
        return True
    return False

  def update_delivery_instructions(self, order, instructions: str) -> bool:
    """
    allows customer to modify delivery instructions
    only works if the order has not progressed too far
    """
    if order.status in ["placed", "preparing"]:
      order.delivery_instructions = instructions
      return True
    return False

class PaymentMethod:
  """
  represent's a customer's payment method
  allows for multiple payment options per customer
  """

  def __init__(self, payment_id: int, card_number: str, card_type: str):
    # identifier for payment method
    self.payment_id = payment_id
    
    # card number is stored as string to avoid potential indexing issues
    self.card_number = card_number

    # card can be either credit or debit
    self.card_type = card_type
