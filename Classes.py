from typing import Optional, List
import mysql.connector

# database connection setup
con = mysql.connector.connect(
  user = 'root',
  host = 'localhost',
  database = 'food_delivery' # placeholder name
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

def sign_up(self) -> bool:
  """
  simulates account registration
  """
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
    for item in self.menu:
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
      order.status = "ready"
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
        self.license_plate = licensePlate

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
            self.current_order = order
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

    def add_item(self, item: MenuItem) -> None:
        """
        adds an item to the order and updates total price
        """
        self.items.append(item)
        self.total_price += item.price

    def remove_item(self, item_id: int) -> bool:
        """
        removes an item from the order by ID
        updates total price accordingly
        """
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                self.total_price -= item.price
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
            return True
        return False

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

    def cancel_order(self) -> bool:
        """
        cancels the order if it hasn't been delivered
        """
        if self.status in ["placed", "preparing"]:
            self.status = "cancelled"
            return True
        return False
  
  class Address:
    """
    represents a physical address used for delivery and location tracking
    now supports international addresses via country field
    """

    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str, unit: str = ""):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.unit = unit  # apartment, suite, etc.

    def __str__(self) -> str:
        """
        returns formatted address string
        adjusts formatting depending on available fields
        """
        parts = [self.street]

        if self.unit:
            parts.append(self.unit)

        parts.append(self.city)

        if self.state:
            parts.append(self.state)

        if self.zip_code:
            parts.append(self.zip_code)

        parts.append(self.country)

        return ", ".join(parts)

    def update_address(self, street: str = None, city: str = None,
                       state: str = None, zip_code: str = None,
                       country: str = None, unit: str = None) -> None:
        """
        updates parts of the address
        """
        if street:
            self.street = street
        if city:
            self.city = city
        if state:
            self.state = state
        if zip_code:
            self.zip_code = zip_code
        if country:
            self.country = country
        if unit is not None:
            self.unit = unit

    def is_same_city(self, other_address) -> bool:
        """
        checks if another address is in the same city AND country
        """
        return (
            self.city.lower() == other_address.city.lower() and
            self.country.lower() == other_address.country.lower()
        )

    def is_same_country(self, other_address) -> bool:
        """
        checks if two addresses are in the same country
        """
        return self.country.lower() == other_address.country.lower()

    def distance_to(self, other_address) -> float:
        """
        placeholder method for distance calculation
        (in real systems, this would use GPS coordinates or an API)
        """
        if self.country != other_address.country:
            return float("inf")  # unrealistic to deliver internationally

        if self.zip_code == other_address.zip_code:
            return 1.0

        return 5.0
