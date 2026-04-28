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
