-- MySQL dump 10.13  Distrib 5.1.51, for pc-linux-gnu (i686)
--
-- Host: 127.0.0.1    Database: world
-- ------------------------------------------------------
-- Server version       5.1.51-debug-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES latin1 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP SCHEMA IF EXISTS book_bay;
CREATE SCHEMA book_bay;
USE book_bay;
SET AUTOCOMMIT=0;

drop table if exists User;
drop table if exists Login_Credential;
drop table if exists Book;
drop table if exists request;
drop table if exists My_Books;
drop table if exists Book_Review;
drop table if exists history;
drop table if exists User_Phone_Number;

CREATE TABLE User
(
  User_ID VARCHAR(20) NOT NULL,
  Name VARCHAR(20) NOT NULL,
  Email_Address VARCHAR(30) NOT NULL,
  House_Number VARCHAR(10) ,
  Street VARCHAR(20) NOT NULL,
  Locality VARCHAR(30) NOT NULL,
  Postal_Code NUMERIC(6) NOT NULL,
  Landmark VARCHAR(30) ,
  City VARCHAR(30) NOT NULL,
  State VARCHAR(30) NOT NULL,
  PRIMARY KEY (User_ID)
);

CREATE TABLE Login_Credential
(
  Password VARCHAR(30) NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  PRIMARY KEY (User_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Book
(
  ISBN VARCHAR(30) NOT NULL,
  Book_Name VARCHAR(200) NOT NULL,
  Edition INT NOT NULL,
  Author VARCHAR(100) NOT NULL,
  Genre VARCHAR(100),
  PRIMARY KEY (ISBN)
);

CREATE TABLE request
(
  Date_of_Request DATE NOT NULL,
  Request_Message VARCHAR(100),
  Request_ID INT NOT NULL AUTO_INCREMENT,
  time_of_request INT NOT NULL,
  borrow_time_duration INT NOT NULL,
  completion_flag INT NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(30) NOT NULL,
  approved_requestUser_ID VARCHAR(20),
  PRIMARY KEY (Request_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID),
  FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
  FOREIGN KEY (approved_requestUser_ID) REFERENCES User(User_ID)
);

CREATE TABLE My_Books
(
  Repayment_Policy VARCHAR(1000) NOT NULL,
  Availability INT NOT NULL,
  Other_Specifications VARCHAR(1000),
  Security_Money_of_Book INT NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(30) NOT NULL,
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID),
  FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE Book_Review
(
  Rating INT NOT NULL,
  Review VARCHAR(5000),
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(30) NOT NULL,
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID),
  FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE history
(
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(30) NOT NULL,
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID),
  FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE User_Phone_Number
(
  Phone_Number NUMERIC(10) NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  PRIMARY KEY (Phone_Number, User_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);
