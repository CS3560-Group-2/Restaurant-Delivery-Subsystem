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

class Address:
    """
    represents a physical address used for delivery and location tracking
    now supports international addresses via country field
    """

    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def save_to_db(self) -> None:
        """
        inserts address into database
        """
        cur.execute("""INSERT INTO Addresses (AddressID, Street, City, State, ZipCode, County) VALUES (%s, %s, %s, %s, %s, %s)""",
                    (self.address_id,
                     self.street,
                     self.city,
                     self.state,
                     self.zip_code,
                     self.country
                    ))
        con.commit()

    def __str__(self) -> str:
        """
        returns formatted address string
        adjusts formatting depending on available fields
        """
        parts = [self.street]

        parts.append(self.city)

        if self.state:
            parts.append(self.state)

        if self.zip_code:
            parts.append(self.zip_code)

        parts.append(self.country)

        return ", ".join(parts)

    def update_address(self, street: str = None, city: str = None,
                       state: str = None, zip_code: str = None,
                       country: str = None) -> None:
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

        cur.execute("""UPDATE Addresses SET Street = %s, City = %s, State = %s, ZipCode = %s, Country = %s WHERE AddressID = %s""", (
           street,
           city,
           state,
           zip_code,
           country,
           self.address_id
        ))
        con.commit()

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
