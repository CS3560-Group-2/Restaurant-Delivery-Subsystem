class Customer(User):
  """
  represents a customer placing delivery orders
  extends User class with functionality such as payment methods and order interaction
  """

  def __init__(self, accountID: int, address: Address, name: str):
    super().__init__(accountID, name)

    # customer's delivery address
    self.address = address

    # 
