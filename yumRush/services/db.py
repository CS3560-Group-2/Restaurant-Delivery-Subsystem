import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "yumrush_user",
    "password": "change_me_now",
    "database": "yumrush",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL UNIQUE,
            address VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id INT NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def create_restaurant(name: str, username: str, address: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO restaurants (name, username, address)
        VALUES (%s, %s, %s)
        """,
        (name, username, address),
    )

    conn.commit()
    restaurant_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return restaurant_id


def update_restaurant_info(restaurant_id: int, name: str, username: str, address: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE restaurants
        SET name = %s, username = %s, address = %s
        WHERE id = %s
        """,
        (name, username, address, restaurant_id),
    )

    conn.commit()
    cursor.close()
    conn.close()


def add_menu_item(restaurant_id: int, item_name: str, price: float) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO menu_items (restaurant_id, item_name, price)
        VALUES (%s, %s, %s)
        """,
        (restaurant_id, item_name, price),
    )

    conn.commit()
    cursor.close()
    conn.close()


def update_menu_item(item_id: int, item_name: str, price: float) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE menu_items
        SET item_name = %s, price = %s
        WHERE id = %s
        """,
        (item_name, price, item_id),
    )

    conn.commit()
    cursor.close()
    conn.close()


def delete_menu_item(item_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_menu_items(restaurant_id: int) -> list[tuple]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, item_name, price
        FROM menu_items
        WHERE restaurant_id = %s
        ORDER BY id
        """,
        (restaurant_id,),
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows
