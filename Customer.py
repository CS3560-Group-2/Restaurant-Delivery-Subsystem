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
