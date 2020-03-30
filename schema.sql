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

drop table if exists user;
drop table if exists login_credential;
drop table if exists book;
drop table if exists request;
drop table if exists my_books;
drop table if exists book_review;
drop table if exists history;
drop table if exists user_phone_number;

CREATE TABLE user
(
  User_ID VARCHAR(20) NOT NULL,
  Name TEXT NOT NULL,
  Email_Address VARCHAR(40) NOT NULL,
  House_Number VARCHAR(10) ,
  Street TEXT NOT NULL,
  Locality TEXT NOT NULL,
  Postal_Code NUMERIC(6) NOT NULL,
  Landmark TEXT ,
  City TEXT NOT NULL,
  State TEXT NOT NULL,
  PRIMARY KEY (User_ID)
);

CREATE TABLE login_credential
(
  Password VARCHAR(30) NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  PRIMARY KEY (User_ID),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID)
);

CREATE TABLE book
(
  ISBN VARCHAR(13) NOT NULL,
  Book_Name TEXT NOT NULL,
  Year INT(4),
  Author TEXT,
  Language CHAR(30),
  PRIMARY KEY (ISBN)
);

CREATE TABLE request
(
  Date_of_Request DATETIME NOT NULL,
  Request_Message TEXT,
  Request_ID INT NOT NULL AUTO_INCREMENT,
  borrow_time_duration INT NOT NULL,
  completion_flag INT NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(30) NOT NULL,
  Requested_User_ID VARCHAR(20),
  PRIMARY KEY (Request_ID),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID),
  FOREIGN KEY (ISBN) REFERENCES book(ISBN),
  FOREIGN KEY (Requested_User_ID) REFERENCES user(User_ID)
);

CREATE TABLE my_books
(
  Repayment_Policy TEXT NOT NULL,
  Availability INT NOT NULL,
  Other_Specifications TEXT,
  Security_Money_of_Book INT NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(13) NOT NULL,
  CHECK (Availability in (0,1)),
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID),
  FOREIGN KEY (ISBN) REFERENCES book(ISBN)
);

CREATE TABLE book_review
(
  Rating INT NOT NULL,
  Review TEXT,
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(13) NOT NULL,
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID),
  FOREIGN KEY (ISBN) REFERENCES book(ISBN)
);

CREATE TABLE history
(
  User_ID VARCHAR(20) NOT NULL,
  ISBN VARCHAR(13) NOT NULL,
  PRIMARY KEY (User_ID, ISBN),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID),
  FOREIGN KEY (ISBN) REFERENCES book(ISBN)
);

CREATE TABLE user_phone_number
(
  Phone_Number NUMERIC(10) NOT NULL,
  User_ID VARCHAR(20) NOT NULL,
  Is_Primary INT NOT NULL,
  PRIMARY KEY (Phone_Number, User_ID),
  FOREIGN KEY (User_ID) REFERENCES user(User_ID)
);
