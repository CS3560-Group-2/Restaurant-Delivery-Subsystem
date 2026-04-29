# Garrison Manson
# Group Assignment #3
# Use cases 7, 8, 9

from __future__ import annotations

from AppUser import AppUser
from Order import Order
from Driver import Driver

# connect database
import mysql.connector
con = mysql.connector.connect(
    user = 'root',
    host = 'localhost',
    database = 'YumRush',
    passwd = 'gmanson')

cur = con.cursor()
        
        
        
class System:
    # Use Case: driver is assigned to delivery once ticket is created
    def driverAssigned(self, order):

        # Find an available driver
        cur.execute("""
            SELECT UserID, LicensePlate, Rating, Status
            FROM Driver
            WHERE Status = 'available'
            LIMIT 1
        """)
        row = cur.fetchone()

        if not row:
            print("No available drivers.")
            return None

        driver_id, license_plate, rating, status = row
        
        # Assign driver to order
        cur.execute("""
            UPDATE Orders
            SET DriverID = %s, Status = 'assigned'
            WHERE OrderID = %s
        """, (driver_id, order_id))

        # Check if order exists
        if cur.rowcount == 0:
            print("Order not found.")
            return None

        # Update driver status
        cur.execute("""
            UPDATE Driver
            SET Status = 'unavailable'
            WHERE UserID = %s
        """, (driver_id,))

        con.commit()

        # Create and link Driver object to Order
        driver_obj = Driver(
            accountID = driver_id,
            licensePlate = license_plate,
            rating = rating,
            status = "unavailable"
        )
        order.driver = driver_obj

        return driver_obj

        print(f"Driver {driver_id} assigned to order {order_id}")
        return driver_id


        
    # Use Case: driver picks up order from restaurant
    def driverArrivesAtRestaurant(self, order):

        # Update order status in database
        cur.execute("""
            UPDATE Orders
            SET Status = 'in route'
            WHERE OrderID = %s
        """, (order.orderID,))

        # Check if order exists
        if cur.rowcount == 0:
            print("Order not found.")
            return None

        con.commit()

        order.status = "in route"

        return None


    
    # Use Case: driver arrives at delivery address
    def driverArrivesAtLocation(self, order):

        driver = order.driver
        # Update order status in database
        cur.execute("""
            UPDATE Orders
            SET Status = 'arrived'
            WHERE OrderID = %s
        """, (order.orderID,))

        # Check if order exists
        if cur.rowcount == 0:
            print("Order not found.")
            return None

        # Set driver back to available
        cur.execute("""
            UPDATE Driver
            SET Status = 'available'
            WHERE UserID = %s
        """, (driver.accountID,))

        con.commit()

        order.status = "arrived"
        driver.status = "available"

        return None
