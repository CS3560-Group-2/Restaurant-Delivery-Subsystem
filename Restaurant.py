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
  
