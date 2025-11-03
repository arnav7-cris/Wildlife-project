USE WildlifeDB;

CREATE INDEX idx_sightings_date ON Sightings(DateSeen);
CREATE INDEX idx_sightings_species ON Sightings(SpeciesID);
CREATE INDEX idx_sightings_location ON Sightings(LocationID);
