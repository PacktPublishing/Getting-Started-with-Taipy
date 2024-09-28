------------------------------------------------
-- SQL code to create the PostgreSQL database --
-- Tot 10 biggest cities of the World         --
------------------------------------------------
-- 1. Create tablesDROP TABLE IF EXISTS CITIES;
DROP TABLE IF EXISTS CITIES;

DROP TABLE IF EXISTS COUNTRY;

-- Create the COUNTRY table
CREATE TABLE
    COUNTRIES (
        CountryID SERIAL PRIMARY KEY,
        CountryName TEXT NOT NULL
    );

-- Create the CITIES table with a foreign key referencing COUNTRY
CREATE TABLE
    CITIES (
        Ranking INTEGER PRIMARY KEY,
        City TEXT NOT NULL,
        CountryID INTEGER,
        Population INTEGER,
        FOREIGN KEY (CountryID) REFERENCES COUNTRIES (CountryID)
    );

-- 2. Insert values 
INSERT INTO
    COUNTRIES (CountryName)
VALUES
    ('Japan'),
    ('India'),
    ('China'),
    ('Brazil'),
    ('Mexico'),
    ('Egypt'),
    ('Bangladesh');

INSERT INTO
    CITIES (Ranking, City, CountryID, Population)
VALUES
    (1, 'Tokyo', 1, 37468000),
    (2, 'Delhi', 2, 28514000),
    (3, 'Shanghai', 3, 25582000),
    (4, 'São Paulo', 4, 21650000),
    (5, 'Mexico City', 5, 21581000),
    (6, 'Cairo', 6, 20076000),
    (7, 'Mumbai', 2, 19980000),
    (8, 'Beijing', 3, 19618000),
    (9, 'Dhaka', 7, 19578000),
    (10, 'Osaka', 1, 19281000);