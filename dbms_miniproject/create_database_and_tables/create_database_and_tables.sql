CREATE DATABASE WildlifeDB;
USE WildlifeDB;

CREATE TABLE Species (
    SpeciesID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Category VARCHAR(30),
    Status VARCHAR(20)
);

CREATE TABLE Locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    LocationName VARCHAR(50),
    Region VARCHAR(50),
    HabitatType VARCHAR(30)
);

CREATE TABLE Rangers (
    RangerID INT AUTO_INCREMENT PRIMARY KEY,
    RangerName VARCHAR(50),
    ContactNo VARCHAR(15),
    AssignedRegion VARCHAR(50)
);

CREATE TABLE Sightings (
    SightingID INT AUTO_INCREMENT PRIMARY KEY,
    SpeciesID INT,
    LocationID INT,
    RangerID INT,
    DateSeen DATE,
    Quantity INT,
    Notes VARCHAR(100),
    FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID),
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
    FOREIGN KEY (RangerID) REFERENCES Rangers(RangerID)
);

-- 5) Alerts table: created by trigger when endangered species is sighted
CREATE TABLE IF NOT EXISTS Alerts (
  AlertID INT PRIMARY KEY AUTO_INCREMENT,
  SpeciesID INT NOT NULL,
  LocationID INT NOT NULL,
  RangerID INT,
  DateSeen DATE,
  Message VARCHAR(255),
  FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID),
  FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
  FOREIGN KEY (RangerID) REFERENCES Rangers(RangerID)
);
