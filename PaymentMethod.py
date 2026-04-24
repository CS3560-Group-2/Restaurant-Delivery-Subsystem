class PaymentMethod:
  """
  represent's a customer's payment method
  allows for multiple payment options per customer
  """

  def __init__(self, payment_id: int, card_number: str, expiry: str):
    self.payment_id = payment_id
    self.card_number = card_number
    self.expiry = expiry
