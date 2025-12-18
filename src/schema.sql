-- =====================================================
-- The Olympian Codex Database Schema
-- Team 42: RNA
-- Phase 4: Database Implementation
-- =====================================================

-- Drop and create database
DROP DATABASE IF EXISTS olympian_codex_db;
CREATE DATABASE olympian_codex_db;
USE olympian_codex_db;

-- =====================================================
-- STRONG ENTITY TABLES
-- =====================================================

-- Table: God
-- Represents the divine entities in the Greek pantheon
CREATE TABLE God (
    Divine_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Domain VARCHAR(100),
    Symbol_of_Power VARCHAR(100),
    Roman_Counterpart VARCHAR(100)
) ENGINE=InnoDB;

-- Table: Demigod
-- Represents the half-blood children of gods
CREATE TABLE Demigod (
    Hero_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Divine_Parent_ID INT NULL,  -- NULLABLE to resolve insertion anomaly
    Date_of_Birth DATE,
    Fatal_Flaw VARCHAR(100),
    Date_of_Arrival DATE,
    Status ENUM('Active', 'Deceased', 'Missing', 'Retired') NOT NULL DEFAULT 'Active',
    FOREIGN KEY (Divine_Parent_ID) REFERENCES God(Divine_ID) 
        ON DELETE SET NULL  -- Resolves deletion anomaly
        ON UPDATE CASCADE,
    INDEX idx_divine_parent (Divine_Parent_ID),
    INDEX idx_status (Status)
) ENGINE=InnoDB;

-- Table: Monster
-- Represents the mythological creatures and threats
CREATE TABLE Monster (
    Monster_ID INT AUTO_INCREMENT PRIMARY KEY,
    Species VARCHAR(100) NOT NULL,
    Threat_Level INT NOT NULL CHECK (Threat_Level BETWEEN 1 AND 10),
    INDEX idx_threat_level (Threat_Level)
) ENGINE=InnoDB;

-- Table: Prophecy
-- Represents prophecies issued by the Oracle of Delphi
CREATE TABLE Prophecy (
    Prophecy_ID INT AUTO_INCREMENT PRIMARY KEY,
    Full_Text TEXT NOT NULL,
    Date_Issued DATE NOT NULL,
    Status ENUM('Pending', 'In Progress', 'Fulfilled', 'Failed') NOT NULL DEFAULT 'Pending',
    INDEX idx_status (Status),
    INDEX idx_date_issued (Date_Issued)
) ENGINE=InnoDB;

-- Table: Quest
-- Represents heroic quests undertaken by demigods
CREATE TABLE Quest (
    Quest_ID INT AUTO_INCREMENT PRIMARY KEY,
    Objective TEXT NOT NULL,
    Prophecy_ID INT UNIQUE,  -- 1:1 relationship with Prophecy
    Start_Date DATE,
    End_Date DATE,
    Outcome ENUM('Success', 'Failure', 'Ongoing', 'Abandoned') DEFAULT 'Ongoing',
    FOREIGN KEY (Prophecy_ID) REFERENCES Prophecy(Prophecy_ID)
        ON DELETE RESTRICT  -- Cannot delete a prophecy if quest exists
        ON UPDATE CASCADE,
    CHECK (End_Date IS NULL OR End_Date >= Start_Date),
    INDEX idx_prophecy (Prophecy_ID),
    INDEX idx_outcome (Outcome)
) ENGINE=InnoDB;

-- Table: Divine_Artifact
-- Represents magical items and weapons of power
CREATE TABLE Divine_Artifact (
    Artifact_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT,
    Current_Wielder INT NULL,  -- Can be unwielded
    FOREIGN KEY (Current_Wielder) REFERENCES Demigod(Hero_ID)
        ON DELETE SET NULL  -- Artifact becomes unwielded if hero dies/deleted
        ON UPDATE CASCADE,
    INDEX idx_wielder (Current_Wielder)
) ENGINE=InnoDB;

-- =====================================================
-- SUBCLASS TABLES (God Hierarchy)
-- =====================================================

-- Table: Olympian
-- Represents the twelve major Olympian gods
CREATE TABLE Olympian (
    Divine_ID INT PRIMARY KEY,
    Council_Seat_Number INT UNIQUE CHECK (Council_Seat_Number BETWEEN 1 AND 12),
    Palace_Location VARCHAR(100),
    FOREIGN KEY (Divine_ID) REFERENCES God(Divine_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Chthonic_God
-- Represents underworld and earth deities
CREATE TABLE Chthonic_God (
    Divine_ID INT PRIMARY KEY,
    Underworld_Domain VARCHAR(100),
    Associated_River VARCHAR(50),
    FOREIGN KEY (Divine_ID) REFERENCES God(Divine_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Primordial
-- Represents the ancient primordial deities
CREATE TABLE Primordial (
    Divine_ID INT PRIMARY KEY,
    Creation_Aspect VARCHAR(100),
    Era_of_Power VARCHAR(50),
    FOREIGN KEY (Divine_ID) REFERENCES God(Divine_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =====================================================
-- SUBCLASS TABLES (Monster Hierarchy)
-- =====================================================

-- Table: Beast
-- Represents physical monster creatures
CREATE TABLE Beast (
    Monster_ID INT PRIMARY KEY,
    Physical_Description TEXT,
    Natural_Habitat VARCHAR(100),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Titan
-- Represents the powerful Titan entities
CREATE TABLE Titan (
    Monster_ID INT PRIMARY KEY,
    Titan_Name VARCHAR(100) NOT NULL,
    Domain_of_Rule VARCHAR(100),
    Imprisonment_Location VARCHAR(100),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Spirit
-- Represents ethereal and spiritual entities
CREATE TABLE Spirit (
    Monster_ID INT PRIMARY KEY,
    Ethereal_Form BOOLEAN DEFAULT TRUE,
    Binding_Object VARCHAR(100),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =====================================================
-- WEAK ENTITY TABLES
-- =====================================================

-- Table: Quest_Log
-- Weak entity: Links demigods to quests with their roles
CREATE TABLE Quest_Log (
    Hero_ID INT,
    Quest_ID INT,
    Role VARCHAR(50),
    Outcome ENUM('Survived', 'Deceased', 'Abandoned', 'Ongoing') DEFAULT 'Ongoing',
    PRIMARY KEY (Hero_ID, Quest_ID),
    FOREIGN KEY (Hero_ID) REFERENCES Demigod(Hero_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Quest_ID) REFERENCES Quest(Quest_ID)
        ON DELETE CASCADE  -- If quest deleted, remove all participant logs
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Sighting_Log
-- Weak entity: Tracks specific monster sightings
CREATE TABLE Sighting_Log (
    Monster_ID INT,
    Sighting_Timestamp DATETIME,
    Location VARCHAR(200) NOT NULL,
    Reported_By INT,
    PRIMARY KEY (Monster_ID, Sighting_Timestamp),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Reported_By) REFERENCES Demigod(Hero_ID)
        ON DELETE SET NULL  -- Preserve sighting even if reporter deleted
        ON UPDATE CASCADE,
    INDEX idx_location (Location),
    INDEX idx_timestamp (Sighting_Timestamp)
) ENGINE=InnoDB;

-- =====================================================
-- MULTI-VALUED ATTRIBUTE TABLES
-- =====================================================

-- Table: Known_Abilities
-- Stores the multi-valued abilities of demigods
CREATE TABLE Known_Abilities (
    Hero_ID INT,
    Ability VARCHAR(100),
    PRIMARY KEY (Hero_ID, Ability),
    FOREIGN KEY (Hero_ID) REFERENCES Demigod(Hero_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Known_Weaknesses
-- Stores the multi-valued weaknesses of monsters
CREATE TABLE Known_Weaknesses (
    Monster_ID INT,
    Weakness VARCHAR(100),
    PRIMARY KEY (Monster_ID, Weakness),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Common_Habitats
-- Stores the multi-valued habitats where monsters are found
CREATE TABLE Common_Habitats (
    Monster_ID INT,
    Habitat VARCHAR(100),
    PRIMARY KEY (Monster_ID, Habitat),
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table: Magical_Properties
-- Stores the multi-valued magical properties of divine artifacts
CREATE TABLE Magical_Properties (
    Artifact_ID INT,
    Property VARCHAR(150),
    PRIMARY KEY (Artifact_ID, Property),
    FOREIGN KEY (Artifact_ID) REFERENCES Divine_Artifact(Artifact_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =====================================================
-- RELATIONSHIP TABLES (M:N Relationships)
-- =====================================================

-- Table: Encounters
-- M:N relationship: Tracks which demigods have encountered which monsters
CREATE TABLE Encounters (
    Hero_ID INT,
    Monster_ID INT,
    Encounter_Date DATE,
    Location VARCHAR(200),
    Outcome ENUM('Victory', 'Defeat', 'Escape', 'Stalemate'),
    PRIMARY KEY (Hero_ID, Monster_ID, Encounter_Date),
    FOREIGN KEY (Hero_ID) REFERENCES Demigod(Hero_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_encounter_date (Encounter_Date)
) ENGINE=InnoDB;

-- Table: Combat_Encounter
-- Complex M:N relationship: Specific combat events involving demigod, artifact, monster, and quest
CREATE TABLE Combat_Encounter (
    Encounter_ID INT AUTO_INCREMENT PRIMARY KEY,
    Hero_ID INT NOT NULL,
    Artifact_ID INT,
    Monster_ID INT NOT NULL,
    Quest_ID INT,
    Combat_Date DATETIME NOT NULL,
    Combat_Location VARCHAR(200),
    Result ENUM('Hero Victory', 'Monster Victory', 'Draw', 'Interrupted'),
    Notes TEXT,
    FOREIGN KEY (Hero_ID) REFERENCES Demigod(Hero_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Artifact_ID) REFERENCES Divine_Artifact(Artifact_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Quest_ID) REFERENCES Quest(Quest_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX idx_combat_date (Combat_Date),
    INDEX idx_hero (Hero_ID),
    INDEX idx_monster (Monster_ID)
) ENGINE=InnoDB;

-- Table: Rescue_Mission
-- Complex M:N relationship: Captures rescue missions involving demigods, quests, gods, and monsters
CREATE TABLE Rescue_Mission (
    Mission_ID INT AUTO_INCREMENT PRIMARY KEY,
    Hero_ID INT NOT NULL,
    Quest_ID INT NOT NULL,
    God_Being_Rescued INT,
    Captor_Monster_ID INT,
    Mission_Date DATE NOT NULL,
    Mission_Location VARCHAR(200),
    Mission_Success BOOLEAN,
    FOREIGN KEY (Hero_ID) REFERENCES Demigod(Hero_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Quest_ID) REFERENCES Quest(Quest_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (God_Being_Rescued) REFERENCES God(Divine_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (Captor_Monster_ID) REFERENCES Monster(Monster_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX idx_mission_date (Mission_Date),
    INDEX idx_quest (Quest_ID)
) ENGINE=InnoDB;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

-- Display confirmation message
SELECT 'The Olympian Codex database schema created successfully!' AS Status;