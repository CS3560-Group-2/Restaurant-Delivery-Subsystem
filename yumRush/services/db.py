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

        #cursor.execute("DROP TABLE IF EXISTS menu_items")
        #cursor.execute("DROP TABLE IF EXISTS menuitem")
        #cursor.execute("DROP TABLE IF EXISTS restaurants")
        #cursor.execute("DROP TABLE IF EXISTS customers")
        #cursor.execute("DROP TABLE IF EXISTS drivers")
        #cursor.execute("DROP TABLE IF EXISTS users")
        #cursor.execute("DROP TABLE IF EXISTS address")
        

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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                OrderID INT NOT NULL AUTO_INCREMENT,
                CustomerID INT NOT NULL,
                RestaurantID INT NOT NULL,
                DriverID INT DEFAULT NULL,
                TotalCost INT DEFAULT 0,
                Status VARCHAR(45) DEFAULT 'Placed',
                PRIMARY KEY (OrderID),
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID),
                FOREIGN KEY (DriverID) REFERENCES drivers(DriverID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                OrderItemID INT NOT NULL AUTO_INCREMENT,
                OrderID INT NOT NULL,
                MenuItemID INT NOT NULL,
                Quantity INT NOT NULL,
                PRIMARY KEY (OrderItemID),
                FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
                FOREIGN KEY (MenuItemID) REFERENCES menuitem(MenuItemID)
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

def delete_customer_account(customer_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT AddressID FROM customers WHERE CustomerID = %s", (customer_id,))
        result = cursor.fetchone()

        cursor.execute("DELETE FROM customers WHERE CustomerID = %s", (customer_id,))
        cursor.execute("DELETE FROM users WHERE UserID = %s AND Type = 'Customer'", (customer_id,))

        if result is not None and result[0] is not None:
            cursor.execute("DELETE FROM address WHERE AddressID = %s", (result[0],))

        conn.commit()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def get_restaurant_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                u.UserID,
                u.Type,
                u.Name,
                u.Username,
                r.RestaurantID,
                r.Address AS AddressID,
                a.Street,
                a.City,
                a.State,
                a.ZIP,
                a.Country
            FROM users u
            JOIN restaurants r
                ON u.UserID = r.RestaurantID
            LEFT JOIN address a
                ON r.Address = a.AddressID
            WHERE u.Username = %s
              AND u.Type = 'Restaurant'
            LIMIT 1
        """, (username,))
        return cursor.fetchone()
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

def update_restaurant_info(
    restaurant_id: int,
    name: str,
    username: str,
    street: str,
    city: str,
    state: str,
    zip_code: int,
    country: str
) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT Address
            FROM restaurants
            WHERE RestaurantID = %s
            """,
            (restaurant_id,)
        )
        result = cursor.fetchone()

        if result is None:
            raise Exception("Restaurant not found.")

        address_id = result[0]

        cursor.execute(
            """
            UPDATE users
            SET Name = %s, Username = %s
            WHERE UserID = %s AND Type = 'Restaurant'
            """,
            (name, username, restaurant_id)
        )

        cursor.execute(
            """
            UPDATE address
            SET Street = %s, City = %s, State = %s, ZIP = %s, Country = %s
            WHERE AddressID = %s
            """,
            (street, city, state, zip_code, country, address_id)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def delete_restaurant_account(restaurant_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT Address FROM restaurants WHERE RestaurantID = %s",
            (restaurant_id,)
        )
        result = cursor.fetchone()

        # delete menu items first (avoid FK issues)
        cursor.execute(
            "DELETE FROM menuitem WHERE Restaurant = %s",
            (restaurant_id,)
        )

        # delete restaurant
        cursor.execute(
            "DELETE FROM restaurants WHERE RestaurantID = %s",
            (restaurant_id,)
        )

        # delete user account
        cursor.execute(
            "DELETE FROM users WHERE UserID = %s AND Type = 'Restaurant'",
            (restaurant_id,)
        )

        # delete address if exists
        if result and result[0]:
            cursor.execute(
                "DELETE FROM address WHERE AddressID = %s",
                (result[0],)
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def get_all_restaurants():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                u.UserID,
                u.Name,
                u.Username,
                r.RestaurantID,
                r.Address
            FROM restaurants r
            JOIN users u ON r.RestaurantID = u.UserID
            WHERE u.Type = 'Restaurant'
            ORDER BY u.Name
        """)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_menu_items_by_restaurant(restaurant_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                MenuItemID,
                Name,
                Cost
            FROM menuitem
            WHERE Restaurant = %s
            ORDER BY Name
        """, (restaurant_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

def create_order(customer_id: int, restaurant_id: int, cart: list[dict]) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT DriverID
            FROM drivers
            WHERE Status = 'Available'
            LIMIT 1
        """)
        driver = cursor.fetchone()

        if driver is None:
            raise Exception("No available drivers right now. Please try again later.")

        driver_id = driver["DriverID"]
        total_cost = sum(item["Cost"] * item["Quantity"] for item in cart)

        cursor.execute("""
            INSERT INTO orders (
                CustomerID,
                RestaurantID,
                DriverID,
                TotalCost,
                Status
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            customer_id,
            restaurant_id,
            driver_id,
            total_cost,
            "Placed"
        ))

        order_id = cursor.lastrowid

        for item in cart:
            cursor.execute("""
                INSERT INTO order_items (
                    OrderID,
                    MenuItemID,
                    Quantity
                )
                VALUES (%s, %s, %s)
            """, (
                order_id,
                item["MenuItemID"],
                item["Quantity"]
            ))

        cursor.execute("""
            UPDATE drivers
            SET Status = 'Busy'
            WHERE DriverID = %s
        """, (driver_id,))

        conn.commit()
        return order_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
