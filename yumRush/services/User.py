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
  def __init__(self, accountID: int, name: str, username: str):
    # user account identifier
    self.accountID = accountID

    # user's actual name
    self.name = name

    # user display name
    self.username = username
    
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
