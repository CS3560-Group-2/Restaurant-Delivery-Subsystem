# Garrison Manson
# Group Assignment #3
# Use cases 7, 8, 9



from __future__ import annotations

# connect database
import mysql.connector
con = mysql.connector.connect(
    user = 'root',
    host = 'localhost',
    database = 'YumRush',
    passwd = 'gmanson')

cur = con.cursor()



class Address:
    # constructor
    def __init__(self, streetNumber: int, streetName: str, city: str, postal_code: int, state: str, country: str):
        self.streetNumber = streetNumber
        self.streetName = streetName
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country



class Customer:
    # constructor
    def __init__(self, accountID: int, address: Address):
        self.accountID = accountID
        self.address = address
    
    # Use Case: customer looks up driver location
    def checkDriverLocation(self, order):
        return order.driver.location



class Restaurant:
    # constructor
    def __init__(self, accountID: int, address: Address):
        self.accountID = accountID
        self.address = address



class Driver:
    # constructor
    def __init__(self, accountID: int, licensePlate: str, location: Address, status: str = "available"):
        self.accountID = accountID
        self.licensePlate = licensePlate
        self.location = location
        self.staus = status
        
        
        
class Order:
    # constructor
    def __init__(self, orderID: int, customer: Customer, restaurant: Restaurant, driver: Driver):
        self.orderID = orderID
        self.status = "assigned"
        self.customer = customer
        self.restaurant = restaurant
        self.driver = driver
        
        
        
class System:
    # Use Case: driver is assigned to delivery once ticket is created
    def driverAssigned(self, order, driver):
        order.driver(driver)
        driver.status("unavailable")
        
    # Use Case: driver picks up order from restaurant
    def driverArrivesAtRestaurant(self, order, driver):
        order.status("in route")
        driver.locaation(order.restaurant)
    
    # Use Case: driver arrives at delivery address
    def driverArrivesAtLocation(self, order):
        driver = order.driver
        driver.status("arrived")
        driver.location(Customer.address)
