# Garrison Manson
# Group Assignment #2
# Use cases 7, 8, 9



from __future__ import annotations



class Address:
    # constructor
    def __init__(self, streetNumber: int, streetName: str, city: str, postal_code: int):
        self.streetNumber = streetNumber
        self.streetName = streetName
        self.city = city
        self.postal_code = postal_code



class Customer:
    # constructor
    def __init__(self, accountID: int, address: Address, name: str, creditCard: int):
        self.accountID = accountID
        self.address = address
        self.name = name
        self.creditCard = creditCard
    
    # Use Case: customer looks up driver location
    def checkDriverLocation(self, order):
        return order.driver.location



class Restaurant:
    # constructor
    def __init__(self, accountID: int, address: Address, name: str):
        self.accountID = accountID
        self.address = address
        self.name = name



class Driver:
    # constructor
    def __init__(self, accountID: int, licensePlate: str, name: str, location: Address, status: str = "available"):
        self.accountID = accountID
        self.licensePlate = licensePlate
        self.name = name
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
        driver.location(customer.address)