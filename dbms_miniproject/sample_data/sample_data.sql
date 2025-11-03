-- sample_data.sql
USE WildlifeDB;

-- Species (explicit IDs for clarity)
INSERT INTO Species (SpeciesID, Name, Category, Status) VALUES
(1,'Bengal Tiger','Mammal','Endangered'),
(2,'Indian Elephant','Mammal','Endangered'),
(3,'Snow Leopard','Mammal','Vulnerable'),
(4,'Indian Peafowl','Bird','Common'),
(5,'One-horned Rhinoceros','Mammal','Endangered'),
(6,'Indian Pangolin','Mammal','Endangered'),
(7,'Spotted Deer','Mammal','Common'),
(8,'King Cobra','Reptile','Vulnerable'),
(9,'Indian Roller','Bird','Common'),
(10,'River Dolphin','Mammal','Endangered'),
(11,'Sloth Bear','Mammal','Vulnerable'),
(12,'Olive Ridley Turtle','Reptile','Vulnerable');

-- Locations
INSERT INTO Locations (LocationID, LocationName, Region, HabitatType) VALUES
(1,'Kaziranga National Park','Assam','Grassland/Wetland'),
(2,'Gir National Park','Gujarat','Dry Deciduous Forest'),
(3,'Sundarbans','West Bengal','Mangrove'),
(4,'Jim Corbett National Park','Uttarakhand','Forest'),
(5,'Hemis National Park','Ladakh','Alpine'),
(6,'Periyar Wildlife Sanctuary','Kerala','Tropical Evergreen');

-- Rangers
INSERT INTO Rangers (RangerID, RangerName, ContactNo, AssignedRegion) VALUES
(1,'Ramesh Patel','9876543210','Gujarat'),
(2,'Anita Kumar','9823456789','Assam'),
(3,'Sanjay Singh','9812345678','Uttarakhand'),
(4,'Meera Desai','9898765432','Kerala'),
(5,'Tsering Dorjee','9860011122','Ladakh');

-- Sightings (explicit SightingID for reproducibility)
INSERT INTO Sightings (SightingID, SpeciesID, LocationID, RangerID, DateSeen, Quantity, Notes) VALUES
(1,1,4,3,'2025-09-10',2,'Tiger with cub'),
(2,4,1,2,'2025-09-12',15,'Group near water'),
(3,3,5,5,'2025-08-20',1,'Single on ridge'),
(4,2,1,2,'2025-07-30',7,'Herd crossing river'),
(5,5,1,2,'2025-08-01',1,'Single rhino near grassland'),
(6,7,1,2,'2025-08-05',30,'Large herd grazing'),
(7,9,6,4,'2025-09-02',5,'Seen by lakeside'),
(8,8,4,3,'2025-06-14',2,'Two near trail'),
(9,10,3,2,'2025-08-15',1,'River dolphin sighted'),
(10,6,6,4,'2025-05-20',1,'Found injured (reported)'),
(11,11,4,3,'2025-04-10',1,'Bear sighting near camp'),
(12,12,3,2,'2025-03-18',12,'Turtle nesting site'),
(13,1,3,2,'2025-02-12',1,'Tiger track found'),
(14,4,2,1,'2025-01-20',8,'Peafowl in grassland'),
(15,7,2,1,'2025-06-25',20,'Deer near waterhole'),
(16,1,4,3,'2025-02-28',1,'Solo tiger seen'),
(17,2,6,4,'2025-04-22',3,'Elephants near sanctuary edge'),
(18,3,5,5,'2025-03-10',2,'Snow leopard tracks'),
(19,8,6,4,'2025-07-07',1,'King cobra near tree roots'),
(20,9,1,2,'2025-09-01',4,'Roller perched on branch'),
(21,5,1,2,'2025-05-02',1,'Rhino grazing'),
(22,6,4,3,'2025-01-15',1,'Pangolin spotted at night'),
(23,10,3,2,'2025-06-03',1,'Dolphin observed bathing'),
(24,11,4,3,'2025-08-11',1,'Sloth bear near campsite');
