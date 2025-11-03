USE WildlifeDB;

--Trigger: when an endangered species sighting is inserted, add an alert
DELIMITER $$
CREATE TRIGGER trg_endangered_alert
AFTER INSERT ON Sightings
FOR EACH ROW
BEGIN
  DECLARE sp_status VARCHAR(20);
  SELECT Status INTO sp_status FROM Species WHERE SpeciesID = NEW.SpeciesID;
  IF sp_status = 'Endangered' THEN
    INSERT INTO Alerts (SpeciesID, LocationID, RangerID, DateSeen, Message)
    VALUES (
      NEW.SpeciesID,
      NEW.LocationID,
      NEW.RangerID,
      NEW.DateSeen,
      CONCAT('Endangered species sighted: ', 
             (SELECT Name FROM Species WHERE SpeciesID = NEW.SpeciesID),
             ' (qty=', NEW.Quantity, ')')
    );
  END IF;
END$$
DELIMITER ;

--  View: join tables for easy reporting
CREATE OR REPLACE VIEW sighting_report AS
SELECT
  si.SightingID,
  s.Name AS Species,
  s.Status AS ConservationStatus,
  l.LocationName,
  l.Region,
  r.RangerName,
  si.DateSeen,
  si.Quantity,
  si.Notes
FROM Sightings si
JOIN Species s ON si.SpeciesID = s.SpeciesID
JOIN Locations l ON si.LocationID = l.LocationID
JOIN Rangers r ON si.RangerID = r.RangerID;

--  Procedure: get sightings by species name
DELIMITER $$
CREATE PROCEDURE get_sightings_by_species(IN sp_name VARCHAR(100))
BEGIN
  SELECT * 
  FROM sighting_report 
  WHERE Species = sp_name 
  ORDER BY DateSeen DESC;
END$$
DELIMITER ;
