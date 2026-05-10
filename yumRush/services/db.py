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
        #cursor.execute("DROP TABLE IF EXISTS order_items")
        #cursor.execute("DROP TABLE IF EXISTS orders")
        

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
                PaymentMethodID INT DEFAULT NULL,
                TotalCost INT DEFAULT 0,
                Status VARCHAR(45) DEFAULT 'Placed',
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (OrderID),
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID),
                FOREIGN KEY (DriverID) REFERENCES drivers(DriverID),
                FOREIGN KEY (PaymentMethodID) REFERENCES payment_methods(PaymentMethodID)
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                PaymentMethodID INT NOT NULL AUTO_INCREMENT,
                CustomerID INT NOT NULL,
                CardName VARCHAR(45),
                CardNumber VARCHAR(20),
                ExpirationDate VARCHAR(10),
                CVV VARCHAR(4),
                PRIMARY KEY (PaymentMethodID),
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurant_reviews (
                ReviewID INT NOT NULL AUTO_INCREMENT,
                OrderID INT NOT NULL,
                CustomerID INT NOT NULL,
                RestaurantID INT NOT NULL,
                Rating INT NOT NULL,
                ReviewText VARCHAR(500),
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ReviewID),
                FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID),
                CONSTRAINT unique_restaurant_review_per_order UNIQUE (OrderID, CustomerID, RestaurantID),
                CONSTRAINT restaurant_rating_range CHECK (Rating BETWEEN 1 AND 5)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS driver_reviews (
                ReviewID INT NOT NULL AUTO_INCREMENT,
                OrderID INT NOT NULL,
                CustomerID INT NOT NULL,
                DriverID INT NOT NULL,
                Rating INT NOT NULL,
                ReviewText VARCHAR(500),
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ReviewID),
                FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                FOREIGN KEY (DriverID) REFERENCES drivers(DriverID),
                CONSTRAINT unique_driver_review_per_order UNIQUE (OrderID, CustomerID, DriverID),
                CONSTRAINT driver_rating_range CHECK (Rating BETWEEN 1 AND 5)
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
        cursor.execute("DELETE FROM payment_methods WHERE CustomerID = %s",(customer_id,))
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

def create_order(customer_id: int, restaurant_id: int, payment_method_id: int, cart: list[dict]) -> int:
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
                PaymentMethodID,
                TotalCost,
                Status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            customer_id,
            restaurant_id,
            driver_id,
            payment_method_id,
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
            SET Status = 'unavailable'
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

def get_customer_order_history(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                o.OrderID,
                o.CustomerID,
                o.RestaurantID,
                o.DriverID,
                o.TotalCost,
                o.Status,
                o.CreatedAt,
                u.Name AS RestaurantName
            FROM orders o
            JOIN users u ON o.RestaurantID = u.UserID
            WHERE o.CustomerID = %s
            ORDER BY o.CreatedAt DESC
        """, (customer_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_order_details(order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                o.OrderID,
                o.CustomerID,
                o.RestaurantID,
                o.DriverID,
                o.TotalCost,
                o.Status,
                o.CreatedAt,
                ruser.Name AS RestaurantName,
                cuser.Name AS CustomerName,
                duser.Name AS DriverName,
                pm.CardName AS PaymentCardName,
                pm.CardNumber AS PaymentCardNumber
            FROM orders o
            JOIN users ruser ON o.RestaurantID = ruser.UserID
            JOIN users cuser ON o.CustomerID = cuser.UserID
            LEFT JOIN users duser ON o.DriverID = duser.UserID
            LEFT JOIN payment_methods pm ON o.PaymentMethodID = pm.PaymentMethodID
            WHERE o.OrderID = %s
        """, (order_id,))

        order = cursor.fetchone()

        cursor.execute("""
            SELECT
                oi.Quantity,
                mi.Name,
                mi.Cost
            FROM order_items oi
            JOIN menuitem mi ON oi.MenuItemID = mi.MenuItemID
            WHERE oi.OrderID = %s
        """, (order_id,))

        items = cursor.fetchall()

        return {
            "order": order,
            "items": items
        }

    finally:
        cursor.close()
        conn.close()

def create_payment_method(customer_id, card_name, card_number, expiration_date, cvv):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO payment_methods (
                CustomerID, CardName, CardNumber, ExpirationDate, CVV
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, card_name, card_number, expiration_date, cvv))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def get_payment_methods(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM payment_methods
            WHERE CustomerID = %s
            ORDER BY PaymentMethodID DESC
        """, (customer_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def delete_payment_method(payment_method_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM payment_methods
            WHERE PaymentMethodID = %s
        """, (payment_method_id,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def get_assigned_order_for_driver(driver_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                o.OrderID,
                o.Status,
                ru.Name AS RestaurantName,
                ra.Street AS RestaurantStreet,
                ra.City AS RestaurantCity,
                ra.State AS RestaurantState,
                ra.ZIP AS RestaurantZIP,
                ra.Country AS RestaurantCountry,
                cu.Name AS CustomerName,
                ca.Street AS CustomerStreet,
                ca.City AS CustomerCity,
                ca.State AS CustomerState,
                ca.ZIP AS CustomerZIP,
                ca.Country AS CustomerCountry
            FROM orders o
            JOIN restaurants r ON o.RestaurantID = r.RestaurantID
            JOIN users ru ON r.RestaurantID = ru.UserID
            JOIN address ra ON r.Address = ra.AddressID
            JOIN customers c ON o.CustomerID = c.CustomerID
            JOIN users cu ON c.CustomerID = cu.UserID
            JOIN address ca ON c.AddressID = ca.AddressID
            WHERE o.DriverID = %s
              AND o.Status != 'Delivered'
            ORDER BY o.OrderID DESC
            LIMIT 1
        """, (driver_id,))

        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def mark_order_delivered(order_id: int, driver_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE orders
            SET Status = 'Delivered'
            WHERE OrderID = %s AND DriverID = %s
        """, (order_id, driver_id))

        cursor.execute("""
            UPDATE drivers
            SET Status = 'available'
            WHERE DriverID = %s
        """, (driver_id,))

        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def create_restaurant_review(order_id: int, customer_id: int, restaurant_id: int, rating: int, review_text: str = "") -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO restaurant_reviews (
                OrderID, CustomerID, RestaurantID, Rating, ReviewText
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, customer_id, restaurant_id, rating, review_text))

        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def create_driver_review(order_id: int, customer_id: int, driver_id: int, rating: int, review_text: str = "") -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO driver_reviews (
                OrderID, CustomerID, DriverID, Rating, ReviewText
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, customer_id, driver_id, rating, review_text))

        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
