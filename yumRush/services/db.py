import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "yumrush_admin",
    "password": "admin123",
    "database": "yumrush",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        #clears tables before creating them
        # Drop in dependency ORDER

        cursor.execute("DROP TABLE IF EXISTS menu_items")
        cursor.execute("DROP TABLE IF EXISTS menuitem")
        cursor.execute("DROP TABLE IF EXISTS restaurants")
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS drivers")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS address")
        

        # Base tables first
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS address (
                AddressID INT NOT NULL AUTO_INCREMENT,
                Street VARCHAR(45) DEFAULT NULL,
                City VARCHAR(45) DEFAULT NULL,
                State VARCHAR(45) DEFAULT NULL,
                ZIP INT DEFAULT NULL,
                Country VARCHAR(45) DEFAULT NULL,
                PRIMARY KEY (AddressID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UserID INT NOT NULL AUTO_INCREMENT,
                Type VARCHAR(15) DEFAULT NULL,
                Name VARCHAR(45) DEFAULT NULL,
                Username VARCHAR(45) DEFAULT NULL,
                PRIMARY KEY (UserID)
            )
        """)

        # Tables that depend on users/address
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                DriverID INT NOT NULL,
                LicensePlate VARCHAR(7) DEFAULT NULL,
                Status VARCHAR(45) DEFAULT NULL,
                Rating INT DEFAULT NULL,
                PRIMARY KEY (DriverID),
                CONSTRAINT UserIDDriver
                    FOREIGN KEY (DriverID) REFERENCES users(UserID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                RestaurantID INT NOT NULL,
                Address INT DEFAULT NULL,
                PRIMARY KEY (RestaurantID),
                INDEX Address_idx (Address),
                CONSTRAINT AddressRestaurant
                    FOREIGN KEY (Address) REFERENCES address(AddressID),
                CONSTRAINT UserIDRestaurant
                    FOREIGN KEY (RestaurantID) REFERENCES users(UserID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menuitem (
                MenuItemID INT NOT NULL AUTO_INCREMENT,
                Restaurant INT DEFAULT NULL,
                Cost INT DEFAULT NULL,
                Name VARCHAR(45) DEFAULT NULL,
                PRIMARY KEY (MenuItemID),
                INDEX Menu_idx (Restaurant),
                CONSTRAINT RestaurantMenuItem
                    FOREIGN KEY (Restaurant) REFERENCES restaurants(RestaurantID)
            )
        """)

        cursor.execute("""
             CREATE TABLE IF NOT EXISTS customers (
                CustomerID INT NOT NULL,
                AddressID INT DEFAULT NULL,
                PRIMARY KEY (CustomerID),
                INDEX CustomerAddress_idx (AddressID),
                CONSTRAINT UserIDCustomer
                    FOREIGN KEY (CustomerID) REFERENCES users(UserID),
                CONSTRAINT AddressCustomer
                    FOREIGN KEY (AddressID) REFERENCES address(AddressID)
             )
         """) 

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def create_user(user_type: str, name: str, username: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (Type, Name, Username)
            VALUES (%s, %s, %s)
        """, (user_type, name, username))

        conn.commit()
        return cursor.lastrowid

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def create_address(street: str, city: str, state: str, zip_code: int, country: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO address (Street, City, State, ZIP, Country)
            VALUES (%s, %s, %s, %s, %s)
        """, (street, city, state, zip_code, country))

        conn.commit()
        return cursor.lastrowid

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def create_driver(name: str, username: str, license_plate: str,
                  status: str = "available", rating: int = 0) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (Type, Name, Username)
            VALUES (%s, %s, %s)
        """, ("Driver", name, username))

        driver_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO drivers (DriverID, LicensePlate, Status, Rating)
            VALUES (%s, %s, %s, %s)
        """, (driver_id, license_plate, status, rating))

        conn.commit()
        return driver_id

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def create_restaurant(name: str, username: str, address_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (Type, Name, Username)
            VALUES (%s, %s, %s)
        """, ("Restaurant", name, username))

        restaurant_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO restaurants (RestaurantID, Address)
            VALUES (%s, %s)
        """, (restaurant_id, address_id))

        conn.commit()
        return restaurant_id

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def update_restaurant_info(restaurant_id: int, name: str, username: str, address_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET Name = %s, Username = %s
            WHERE UserID = %s AND Type = 'Restaurant'
        """, (name, username, restaurant_id))

        cursor.execute("""
            UPDATE restaurants
            SET Address = %s
            WHERE RestaurantID = %s
        """, (address_id, restaurant_id))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def add_menu_item(restaurant_id: int, item_name: str, price: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO menuitem (Restaurant, Cost, Name)
            VALUES (%s, %s, %s)
        """, (restaurant_id, price, item_name))

        conn.commit()
        return cursor.lastrowid

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def update_menu_item(item_id: int, item_name: str, price: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE menuitem
            SET Name = %s, Cost = %s
            WHERE MenuItemID = %s
        """, (item_name, price, item_id))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def delete_menu_item(item_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM menuitem
            WHERE MenuItemID = %s
        """, (item_id,))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def get_menu_items(restaurant_id: int) -> list[tuple]:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT MenuItemID, Name, Cost
            FROM menuitem
            WHERE Restaurant = %s
            ORDER BY MenuItemID
        """, (restaurant_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

def get_driver_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                u.UserID,
                u.Type,
                u.Name,
                u.Username,
                d.DriverID,
                d.LicensePlate,
                d.Status,
                d.Rating
            FROM users u
            JOIN drivers d
                ON u.UserID = d.DriverID
            WHERE u.Username = %s
              AND u.Type = 'Driver'
            LIMIT 1
        """, (username,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

def update_driver_info(driver_id: int, name: str, username: str, license_plate: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET Name = %s, Username = %s
            WHERE UserID = %s AND Type = 'Driver'
        """, (name, username, driver_id))

        cursor.execute("""
            UPDATE drivers
            SET LicensePlate = %s
            WHERE DriverID = %s
        """, (license_plate, driver_id))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def update_driver_status(driver_id: int, status: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE drivers
            SET Status = %s
            WHERE DriverID = %s
        """, (status, driver_id))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def create_customer(name: str, username: str,
                    street: str, city: str, state: str,
                    zip_code: int, country: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO address (Street, City, State, ZIP, Country)
            VALUES (%s, %s, %s, %s, %s)
        """, (street, city, state, zip_code, country))
        address_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO users (Type, Name, Username)
            VALUES (%s, %s, %s)
        """, ("Customer", name, username))
        customer_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO customers (CustomerID, AddressID)
            VALUES (%s, %s)
        """, (customer_id, address_id))

        conn.commit()
        return customer_id

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def get_customer_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                u.UserID,
                u.Type,
                u.Name,
                u.Username,
                c.CustomerID,
                c.AddressID,
                a.Street,
                a.City,
                a.State,
                a.ZIP,
                a.Country
            FROM users u
            JOIN customers c
                ON u.UserID = c.CustomerID
            LEFT JOIN address a
                ON c.AddressID = a.AddressID
            WHERE u.Username = %s
              AND u.Type = 'Customer'
            LIMIT 1
        """, (username,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def update_customer_info(customer_id: int, name: str, username: str,
                         street: str, city: str, state: str,
                         zip_code: int, country: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET Name = %s, Username = %s
            WHERE UserID = %s AND Type = 'Customer'
        """, (name, username, customer_id))

        cursor.execute("""
            SELECT AddressID
            FROM customers
            WHERE CustomerID = %s
        """, (customer_id,))
        result = cursor.fetchone()

        if result is None:
            raise Exception("Customer profile not found.")

        address_id = result[0]

        cursor.execute("""
            UPDATE address
            SET Street = %s,
                City = %s,
                State = %s,
                ZIP = %s,
                Country = %s
            WHERE AddressID = %s
        """, (street, city, state, zip_code, country, address_id))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def delete_driver_account(driver_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM drivers
            WHERE DriverID = %s
        """, (driver_id,))

        cursor.execute("""
            DELETE FROM users
            WHERE UserID = %s AND Type = 'Driver'
        """, (driver_id,))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
