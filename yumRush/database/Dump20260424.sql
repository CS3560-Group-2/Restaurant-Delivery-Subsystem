-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: yumrush
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `AddressID` int NOT NULL AUTO_INCREMENT,
  `Street` varchar(45) DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `State` varchar(45) DEFAULT NULL,
  `ZIP` int DEFAULT NULL,
  `Country` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AddressID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Address` int DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  KEY `Address_idx` (`Address`),
  CONSTRAINT `AddressCustomer` FOREIGN KEY (`Address`) REFERENCES `address` (`AddressID`),
  CONSTRAINT `UserIDCustomer` FOREIGN KEY (`CustomerID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drivers`
--

DROP TABLE IF EXISTS `drivers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drivers` (
  `DriverID` int NOT NULL AUTO_INCREMENT,
  `LicensePlate` varchar(7) DEFAULT NULL,
  `Location` int DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Rating` int DEFAULT NULL,
  PRIMARY KEY (`DriverID`),
  CONSTRAINT `UserIDDriver` FOREIGN KEY (`DriverID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `LocationID` int NOT NULL AUTO_INCREMENT,
  `Driver` int DEFAULT NULL,
  `Longitude` float DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  PRIMARY KEY (`LocationID`),
  KEY `DriverLocation_idx` (`Driver`),
  CONSTRAINT `DriverLocation` FOREIGN KEY (`Driver`) REFERENCES `drivers` (`DriverID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menuitem`
--

DROP TABLE IF EXISTS `menuitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menuitem` (
  `MenuItemID` int NOT NULL AUTO_INCREMENT,
  `Restaurant` int DEFAULT NULL,
  `Cost` int DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`MenuItemID`),
  KEY `Menu_idx` (`Restaurant`),
  CONSTRAINT `RestaurantMenuItem` FOREIGN KEY (`Restaurant`) REFERENCES `restaurants` (`RestaurantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `OrderItemID` int NOT NULL AUTO_INCREMENT,
  `Order` int DEFAULT NULL,
  `Item` int DEFAULT NULL,
  PRIMARY KEY (`OrderItemID`),
  KEY `Order_idx` (`Order`),
  KEY `Item_idx` (`Item`),
  CONSTRAINT `Item` FOREIGN KEY (`Item`) REFERENCES `menuitem` (`MenuItemID`),
  CONSTRAINT `Order` FOREIGN KEY (`Order`) REFERENCES `orders` (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) DEFAULT NULL,
  `Customer` int DEFAULT NULL,
  `Driver` int DEFAULT NULL,
  `Restaurant` int DEFAULT NULL,
  `Item` int DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `Customer_idx` (`Customer`),
  KEY `Driver_idx` (`Driver`),
  KEY `Restaurant_idx` (`Restaurant`),
  CONSTRAINT `Customer` FOREIGN KEY (`Customer`) REFERENCES `customers` (`CustomerID`),
  CONSTRAINT `Driver` FOREIGN KEY (`Driver`) REFERENCES `drivers` (`DriverID`),
  CONSTRAINT `Restaurant` FOREIGN KEY (`Restaurant`) REFERENCES `restaurants` (`RestaurantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paymentmethod`
--

DROP TABLE IF EXISTS `paymentmethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paymentmethod` (
  `PaymentMethodID` varchar(45) NOT NULL,
  `Customer` int DEFAULT NULL,
  `CardNumber` int DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`PaymentMethodID`),
  KEY `CustomerID` (`Customer`),
  CONSTRAINT `CustomerID` FOREIGN KEY (`Customer`) REFERENCES `customers` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurants` (
  `RestaurantID` int NOT NULL AUTO_INCREMENT,
  `Address` int DEFAULT NULL,
  PRIMARY KEY (`RestaurantID`),
  KEY `Address_idx` (`Address`),
  CONSTRAINT `AddressRestaurant` FOREIGN KEY (`Address`) REFERENCES `address` (`AddressID`),
  CONSTRAINT `UserIDRestaurant` FOREIGN KEY (`RestaurantID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ReviewID` int NOT NULL AUTO_INCREMENT,
  `Order` int DEFAULT NULL,
  `Customer` int DEFAULT NULL,
  `Driver` int DEFAULT NULL,
  `Rating` int DEFAULT NULL,
  `Comments` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ReviewID`),
  KEY `Order_idx` (`Order`),
  KEY `Customer_idx` (`Customer`),
  KEY `Driver_idx` (`Driver`),
  CONSTRAINT `CustomerReview` FOREIGN KEY (`Customer`) REFERENCES `customers` (`CustomerID`),
  CONSTRAINT `DriverReview` FOREIGN KEY (`Driver`) REFERENCES `drivers` (`DriverID`),
  CONSTRAINT `OrderReview` FOREIGN KEY (`Order`) REFERENCES `orders` (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(15) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Username` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-24 17:19:11
