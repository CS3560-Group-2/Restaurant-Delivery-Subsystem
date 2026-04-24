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
