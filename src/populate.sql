-- =====================================================
-- The Olympian Codex Database - Data Population
-- Team 42: RNA
-- Phase 4: Database Implementation
-- =====================================================

USE olympian_codex_db;

-- Disable foreign key checks temporarily for easier insertion
SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================
-- POPULATE GOD TABLE
-- =====================================================

INSERT INTO God (Divine_ID, Name, Domain, Symbol_of_Power, Roman_Counterpart) VALUES
(1, 'Zeus', 'Sky and Thunder', 'Lightning Bolt', 'Jupiter'),
(2, 'Poseidon', 'Sea and Earthquakes', 'Trident', 'Neptune'),
(3, 'Hades', 'Underworld and Death', 'Helm of Darkness', 'Pluto'),
(4, 'Athena', 'Wisdom and Strategy', 'Aegis Shield', 'Minerva'),
(5, 'Apollo', 'Sun and Music', 'Golden Lyre', 'Apollo'),
(6, 'Artemis', 'Hunt and Moon', 'Silver Bow', 'Diana'),
(7, 'Ares', 'War and Violence', 'Spear and Shield', 'Mars'),
(8, 'Aphrodite', 'Love and Beauty', 'Magic Girdle', 'Venus'),
(9, 'Hephaestus', 'Forge and Fire', 'Hammer and Anvil', 'Vulcan'),
(10, 'Hermes', 'Travelers and Thieves', 'Caduceus', 'Mercury'),
(11, 'Dionysus', 'Wine and Madness', 'Thyrsus', 'Bacchus'),
(12, 'Demeter', 'Agriculture and Harvest', 'Cornucopia', 'Ceres'),
(13, 'Hera', 'Marriage and Family', 'Peacock Crown', 'Juno'),
(14, 'Hestia', 'Hearth and Home', 'Sacred Flame', 'Vesta'),
(15, 'Persephone', 'Spring and Underworld Queen', 'Pomegranate', 'Proserpina'),
(16, 'Hecate', 'Magic and Crossroads', 'Torches', 'Trivia'),
(17, 'Thanatos', 'Death', 'Sword', 'Mors'),
(18, 'Nyx', 'Night', 'Star Veil', 'Nox'),
(19, 'Erebus', 'Darkness', 'Shadow Cloak', 'Erebus'),
(20, 'Gaia', 'Earth', 'Living Earth', 'Terra');

-- =====================================================
-- POPULATE GOD SUBCLASS TABLES
-- =====================================================

-- Olympians (The Twelve)
INSERT INTO Olympian (Divine_ID, Council_Seat_Number, Palace_Location) VALUES
(1, 1, 'Throne Room - Center'),
(2, 2, 'Throne Room - East'),
(3, NULL, 'Underworld Palace'),  -- Hades doesn't have a seat
(4, 3, 'Throne Room - North'),
(5, 4, 'Throne Room - South'),
(6, 5, 'Throne Room - West'),
(7, 6, 'Throne Room - Northeast'),
(8, 7, 'Throne Room - Southeast'),
(9, 8, 'Throne Room - Northwest'),
(10, 9, 'Throne Room - Southwest'),
(11, 10, 'Throne Room - East Wing'),
(12, 11, 'Throne Room - West Wing'),
(13, 12, 'Throne Room - Right of Zeus');

-- Chthonic Gods
INSERT INTO Chthonic_God (Divine_ID, Underworld_Domain, Associated_River) VALUES
(3, 'Ruler of the Underworld', 'Styx'),
(15, 'Queen of the Underworld', 'Lethe'),
(16, 'Mistress of Magic', 'Acheron'),
(17, 'Personification of Death', 'Cocytus');

-- Primordials
INSERT INTO Primordial (Divine_ID, Creation_Aspect, Era_of_Power) VALUES
(18, 'Night and Darkness', 'Before Olympus'),
(19, 'Primordial Darkness', 'Before Olympus'),
(20, 'Mother Earth', 'Before Olympus');

-- =====================================================
-- POPULATE DEMIGOD TABLE
-- =====================================================

INSERT INTO Demigod (Hero_ID, First_Name, Last_Name, Divine_Parent_ID, Date_of_Birth, Fatal_Flaw, Date_of_Arrival, Status) VALUES
(1, 'Percy', 'Jackson', 2, '1993-08-18', 'Excessive Personal Loyalty', '2005-06-01', 'Active'),
(2, 'Annabeth', 'Chase', 4, '1993-07-12', 'Hubris', '2000-01-15', 'Active'),
(3, 'Thalia', 'Grace', 1, '1987-12-22', 'Ambition and Pride', '2003-12-21', 'Active'),
(4, 'Nico', 'di Angelo', 3, '1932-01-28', 'Holding Grudges', '2006-03-10', 'Active'),
(5, 'Luke', 'Castellan', 10, '1987-05-06', 'Wrath and Resentment', '1991-08-20', 'Deceased'),
(6, 'Clarisse', 'La Rue', 7, '1990-11-15', 'Pride in Combat', '2000-07-04', 'Active'),
(7, 'Silena', 'Beauregard', 8, '1991-03-25', 'Desire for Acceptance', '2003-05-12', 'Deceased'),
(8, 'Charles', 'Beckendorf', 9, '1989-09-10', 'Overconfidence', '2001-06-18', 'Deceased'),
(9, 'Will', 'Solace', 5, '1994-04-16', 'Excessive Caring', '2006-08-22', 'Active'),
(10, 'Katie', 'Gardner', 12, '1993-06-08', 'Stubbornness', '2005-04-30', 'Active'),
(11, 'Travis', 'Stoll', 10, '1992-11-20', 'Kleptomania', '2003-09-15', 'Active'),
(12, 'Connor', 'Stoll', 10, '1992-11-20', 'Recklessness', '2003-09-15', 'Active'),
(13, 'Piper', 'McLean', 8, '1995-06-03', 'Self-Doubt', '2010-10-12', 'Active'),
(14, 'Jason', 'Grace', 1, '1994-07-01', 'Sense of Duty', '2010-10-12', 'Deceased'),
(15, 'Leo', 'Valdez', 9, '1995-07-07', 'Feeling of Inadequacy', '2010-10-12', 'Active'),
(16, 'Hazel', 'Levesque', 15, '1928-12-17', 'Guilt', '2010-11-20', 'Active'),
(17, 'Frank', 'Zhang', 7, '1995-06-05', 'Self-Doubt', '2010-11-20', 'Active'),
(18, 'Reyna', 'Ramirez-Arellano', 4, '1993-03-14', 'Shouldering Too Much', '2005-07-08', 'Active'),
(19, 'Bianca', 'di Angelo', 3, '1930-04-16', 'Running from Responsibility', '2006-03-10', 'Deceased'),
(20, 'Zoe', 'Nightshade', 6, NULL, 'Distrust of Men', '1000-01-01', 'Deceased'),
(21, 'Malcolm', 'Pace', 4, '1992-08-30', 'Overthinking', '2004-05-20', 'Active'),
(22, 'Butch', 'Walker', 6, '1991-02-14', 'Aggression', '2005-11-11', 'Active'),
(23, 'Drew', 'Tanaka', 8, '1994-10-31', 'Vanity', '2007-02-28', 'Active'),
(24, 'Jake', 'Mason', 9, '1990-12-05', 'Perfectionism', '2003-03-17', 'Active'),
(25, 'Ethan', 'Nakamura', NULL, '1991-07-19', 'Vengeance', '2004-09-22', 'Deceased');

-- =====================================================
-- POPULATE KNOWN_ABILITIES TABLE
-- =====================================================

INSERT INTO Known_Abilities (Hero_ID, Ability) VALUES
(1, 'Water Manipulation'),
(1, 'Underwater Breathing'),
(1, 'Earthquake Generation'),
(1, 'Communication with Horses'),
(2, 'Strategic Genius'),
(2, 'Architecture Expertise'),
(2, 'Weaving'),
(3, 'Lightning Summoning'),
(3, 'Flight'),
(3, 'Electrokinesis'),
(4, 'Shadow Travel'),
(4, 'Umbrakinesis'),
(4, 'Necromancy'),
(4, 'Ghost Summoning'),
(5, 'Expert Swordsmanship'),
(5, 'Persuasion'),
(6, 'Combat Expertise'),
(6, 'Spear Mastery'),
(7, 'Charmspeak'),
(7, 'Beauty Enhancement'),
(8, 'Master Craftsman'),
(8, 'Trap Setting'),
(9, 'Healing'),
(9, 'Archery'),
(9, 'Plague Control'),
(10, 'Chlorokinesis'),
(10, 'Plant Communication'),
(11, 'Thievery'),
(11, 'Lock Picking'),
(12, 'Thievery'),
(12, 'Pranking'),
(13, 'Charmspeak'),
(13, 'Sword Fighting'),
(14, 'Lightning Control'),
(14, 'Flight'),
(14, 'Sword Fighting'),
(15, 'Fire Immunity'),
(15, 'Mechanical Genius'),
(15, 'Pyrokinesis'),
(16, 'Geokinesis'),
(16, 'Precious Metal Control'),
(17, 'Shapeshifting'),
(17, 'Archery'),
(18, 'Leadership'),
(18, 'Combat Expertise'),
(20, 'Archery Mastery'),
(20, 'Immortality'),
(21, 'Strategic Planning'),
(22, 'Flight'),
(23, 'Charmspeak'),
(24, 'Metalworking');

-- =====================================================
-- POPULATE MONSTER TABLE
-- =====================================================

INSERT INTO Monster (Monster_ID, Species, Threat_Level) VALUES
(1, 'Minotaur', 7),
(2, 'Medusa', 8),
(3, 'Chimera', 9),
(4, 'Hydra', 9),
(5, 'Hellhound', 6),
(6, 'Fury', 7),
(7, 'Manticore', 8),
(8, 'Nemean Lion', 9),
(9, 'Cyclops', 5),
(10, 'Empousai', 6),
(11, 'Sphinx', 7),
(12, 'Stymphalian Bird', 5),
(13, 'Scylla', 10),
(14, 'Charybdis', 10),
(15, 'Kronos', 10),
(16, 'Atlas', 10),
(17, 'Hyperion', 9),
(18, 'Krios', 8),
(19, 'Lamia', 6),
(20, 'Dracaena', 5),
(21, 'Cerberus', 9),
(22, 'Typhon', 10),
(23, 'Python', 8),
(24, 'Kampê', 9),
(25, 'Laistrygonian Giant', 7);

-- =====================================================
-- POPULATE MONSTER SUBCLASS TABLES
-- =====================================================

-- Beasts
INSERT INTO Beast (Monster_ID, Physical_Description, Natural_Habitat) VALUES
(1, 'Bull-headed humanoid with bronze skin', 'Labyrinths and Mazes'),
(2, 'Woman with snake hair and petrifying gaze', 'Dark Caves'),
(3, 'Lion head, goat body, serpent tail, fire-breathing', 'Mountains'),
(4, 'Multi-headed serpent that regrows heads', 'Swamps'),
(5, 'Massive black dog with red eyes', 'Underworld Borders'),
(7, 'Lion body, human head, scorpion tail', 'Deserts'),
(8, 'Golden-furred lion with impenetrable hide', 'Valleys'),
(9, 'One-eyed giant', 'Caves and Forges'),
(11, 'Lion body with human head, riddle master', 'Crossroads'),
(12, 'Bronze-beaked birds', 'Swamps'),
(13, 'Six-headed sea serpent', 'Sea Straits'),
(14, 'Giant whirlpool monster', 'Sea Straits'),
(19, 'Vampire-like female monster', 'Dark Places'),
(20, 'Female warrior with snake lower body', 'Various'),
(21, 'Three-headed guard dog of Hades', 'Gates of the Underworld'),
(23, 'Giant serpent', 'Delphi'),
(25, 'Cannibalistic giant', 'Northern Islands');

-- Titans
INSERT INTO Titan (Monster_ID, Titan_Name, Domain_of_Rule, Imprisonment_Location) VALUES
(15, 'Kronos', 'Time and Fate', 'Tartarus'),
(16, 'Atlas', 'Endurance', 'Mount Othrys'),
(17, 'Hyperion', 'Light', 'Tartarus'),
(18, 'Krios', 'Constellations', 'Tartarus'),
(22, 'Typhon', 'Storms', 'Mount Etna'),
(24, 'Kampê', 'Tartarus Guard', 'Tartarus');

-- Spirits
INSERT INTO Spirit (Monster_ID, Ethereal_Form, Binding_Object) VALUES
(6, TRUE, 'Whip'),
(10, TRUE, 'Bronze Legs');

-- =====================================================
-- POPULATE KNOWN_WEAKNESSES TABLE
-- =====================================================

INSERT INTO Known_Weaknesses (Monster_ID, Weakness) VALUES
(1, 'Confined Spaces'),
(1, 'Confusion'),
(2, 'Reflective Surfaces'),
(2, 'Averting Direct Eye Contact'),
(3, 'Water'),
(3, 'Cold'),
(4, 'Cauterizing Wounds'),
(4, 'Fire'),
(5, 'Celestial Bronze'),
(5, 'Sunlight'),
(6, 'Iron'),
(6, 'Holy Water'),
(7, 'Artemis Blessing'),
(8, 'Heracles Strength'),
(9, 'Intelligence'),
(10, 'Celestial Bronze'),
(11, 'Correct Answers to Riddles'),
(12, 'Loud Noises'),
(13, 'Navigation Skills'),
(14, 'Navigation Skills'),
(15, 'Time Manipulation'),
(15, 'Divided Essence'),
(16, 'Removing the Sky Burden'),
(17, 'Sunlight Absence'),
(18, 'Ram-related Magic'),
(19, 'Fire'),
(21, 'Music'),
(22, 'Combined God Power'),
(23, 'Archery'),
(25, 'Fire');

-- =====================================================
-- POPULATE COMMON_HABITATS TABLE
-- =====================================================

INSERT INTO Common_Habitats (Monster_ID, Habitat) VALUES
(1, 'Labyrinths'),
(1, 'Enclosed Spaces'),
(2, 'Caves'),
(2, 'Abandoned Temples'),
(3, 'Mountain Peaks'),
(4, 'Swamps'),
(4, 'Marshlands'),
(5, 'Shadows'),
(5, 'Underworld Entrances'),
(6, 'Sky'),
(6, 'Underworld'),
(7, 'Deserts'),
(7, 'Wastelands'),
(8, 'Valleys'),
(9, 'Caves'),
(9, 'Forges'),
(10, 'Dark Alleys'),
(10, 'Ruins'),
(11, 'Crossroads'),
(12, 'Lakes'),
(12, 'Swamps'),
(13, 'Sea of Monsters'),
(14, 'Sea of Monsters'),
(15, 'Tartarus'),
(16, 'Mount Othrys'),
(17, 'Tartarus'),
(18, 'Tartarus'),
(19, 'Underground'),
(20, 'Various Terrains'),
(21, 'Underworld Gates'),
(22, 'Mount Etna'),
(23, 'Delphi'),
(24, 'Tartarus'),
(25, 'Islands');

-- =====================================================
-- POPULATE PROPHECY TABLE
-- =====================================================

INSERT INTO Prophecy (Prophecy_ID, Full_Text, Date_Issued, Status) VALUES
(1, 'You shall go west, and face the god who has turned. You shall find what was stolen, and see it safely returned. You shall be betrayed by one who calls you a friend. And you shall fail to save what matters most, in the end.', '2005-06-15', 'Fulfilled'),
(2, 'Five shall go west to the goddess in chains. One shall be lost in the land without rain. The bane of Olympus shows the trail. Campers and Hunters combined prevail. The Titan''s curse must one withstand. And one shall perish by a parent''s hand.', '2007-11-20', 'Fulfilled'),
(3, 'A half-blood of the eldest gods shall reach sixteen against all odds. And see the world in endless sleep. The hero''s soul, cursed blade shall reap. A single choice shall end his days. Olympus to preserve or raze.', '1993-08-18', 'Fulfilled'),
(4, 'Seven half-bloods shall answer the call. To storm or fire the world must fall. An oath to keep with a final breath. And foes bear arms to the Doors of Death.', '2010-07-04', 'Fulfilled'),
(5, 'Child of lightning, beware the earth. The giants'' revenge the seven shall birth. The forge and dove shall break the cage. And death unleash through Hera''s rage.', '2010-10-23', 'Fulfilled'),
(6, 'To the north beyond the gods, lies the legion''s crown. Falling from ice, the son of Neptune shall drown.', '2010-06-15', 'Fulfilled'),
(7, 'The Mark of Athena burns through Rome. Twins snuff out the angel''s breath. Who holds the key to endless death. Giants'' bane stands gold and pale. Won through pain from a woven jail.', '2010-11-01', 'Fulfilled'),
(8, 'The dark prophecy yet remains unspoken. When oracles fall, the world is broken.', '2016-05-12', 'Pending'),
(9, 'Go to Alaska. Find Thanatos and free him. Come back by sundown on June twenty-fourth or die.', '2010-12-18', 'Fulfilled'),
(10, 'A new threat rises from the ancient past. The camp must stand united or fall at last.', '2024-03-15', 'Pending');

-- =====================================================
-- POPULATE QUEST TABLE
-- =====================================================

INSERT INTO Quest (Quest_ID, Objective, Prophecy_ID, Start_Date, End_Date, Outcome) VALUES
(1, 'Retrieve Zeus'' Master Bolt from the Underworld', 1, '2005-06-21', '2005-07-04', 'Success'),
(2, 'Rescue Artemis from the Titan Atlas', 2, '2007-12-01', '2007-12-21', 'Success'),
(3, 'Stop Kronos from destroying Olympus', 3, '2009-08-18', '2009-08-18', 'Success'),
(4, 'Close the Doors of Death', 4, '2010-07-05', '2010-08-01', 'Success'),
(5, 'Free Hera and prevent the Giant uprising', 5, '2010-10-24', '2010-12-21', 'Success'),
(6, 'Find and free Thanatos', 6, '2010-12-19', '2010-12-24', 'Success'),
(7, 'Follow the Mark of Athena to Greece', 7, '2011-01-15', '2011-07-15', 'Success'),
(8, 'Investigate disturbances at Delphi', NULL, '2016-06-01', '2016-08-30', 'Success'),
(9, 'Defeat the Colossus Neronis', NULL, '2017-05-12', '2017-05-20', 'Success'),
(10, 'Scout for monster activity near New York', NULL, '2024-04-01', NULL, 'Ongoing'),
(11, 'Clear monsters from Camp borders', NULL, '2024-05-15', '2024-05-16', 'Success'),
(12, 'Investigate ancient ruins in Greece', NULL, '2024-06-20', NULL, 'Ongoing');

-- =====================================================
-- POPULATE QUEST_LOG TABLE
-- =====================================================

INSERT INTO Quest_Log (Hero_ID, Quest_ID, Role, Outcome) VALUES
(1, 1, 'Leader', 'Survived'),
(2, 1, 'Navigator', 'Survived'),
(5, 1, 'Guide', 'Survived'),
(1, 2, 'Member', 'Survived'),
(2, 2, 'Member', 'Survived'),
(3, 2, 'Member', 'Survived'),
(19, 2, 'Hunter', 'Deceased'),
(20, 2, 'Hunter Leader', 'Deceased'),
(1, 3, 'Leader', 'Survived'),
(2, 3, 'Strategist', 'Survived'),
(5, 3, 'Betrayer', 'Deceased'),
(6, 3, 'Warrior', 'Survived'),
(7, 3, 'Spy', 'Deceased'),
(8, 3, 'Saboteur', 'Deceased'),
(1, 4, 'Leader', 'Survived'),
(2, 4, 'Strategist', 'Survived'),
(13, 4, 'Mediator', 'Survived'),
(14, 4, 'Fighter', 'Deceased'),
(15, 4, 'Engineer', 'Survived'),
(16, 4, 'Scout', 'Survived'),
(17, 4, 'Warrior', 'Survived'),
(13, 5, 'Leader', 'Survived'),
(14, 5, 'Leader', 'Survived'),
(15, 5, 'Engineer', 'Survived'),
(17, 6, 'Leader', 'Survived'),
(16, 6, 'Member', 'Survived'),
(1, 7, 'Member', 'Survived'),
(2, 7, 'Leader', 'Survived'),
(13, 7, 'Member', 'Survived'),
(14, 7, 'Member', 'Survived'),
(15, 7, 'Member', 'Survived'),
(16, 7, 'Member', 'Survived'),
(17, 7, 'Member', 'Survived'),
(9, 8, 'Leader', 'Survived'),
(21, 8, 'Strategist', 'Survived'),
(9, 9, 'Healer', 'Survived'),
(4, 9, 'Shadow Scout', 'Survived'),
(1, 10, 'Scout', 'Ongoing'),
(2, 10, 'Strategist', 'Ongoing'),
(6, 11, 'Leader', 'Survived'),
(11, 11, 'Support', 'Survived'),
(12, 11, 'Support', 'Survived'),
(2, 12, 'Leader', 'Ongoing'),
(21, 12, 'Scholar', 'Ongoing');

-- =====================================================
-- POPULATE DIVINE_ARTIFACT TABLE
-- =====================================================

INSERT INTO Divine_Artifact (Artifact_ID, Name, Description, Current_Wielder) VALUES
(1, 'Riptide', 'Celestial bronze sword that returns to owner', 1),
(2, 'Annabeth''s Drakon Bone Sword', 'Sword made from drakon bone', 2),
(3, 'Aegis Shield', 'Shield bearing Medusa''s head, causes fear', 3),
(4, 'Stygian Iron Sword', 'Black sword that can harm mortals and immortals', 4),
(5, 'Backbiter', 'Half steel, half celestial bronze sword', NULL),
(6, 'Maimer', 'Electric spear that returns when thrown', 6),
(7, 'Kronos'' Scythe', 'Powerful scythe of the Titan King', NULL),
(8, 'Master Bolt', 'Zeus'' ultimate lightning weapon', NULL),
(9, 'Poseidon''s Trident', 'Three-pronged spear controlling seas', NULL),
(10, 'Helm of Darkness', 'Makes wearer invisible and terrifying', NULL),
(11, 'Ivlivs', 'Imperial gold sword', NULL),
(12, 'Katoptris', 'Dagger that shows possible futures', 13),
(13, 'Archimedes Sphere', 'Device of immense mechanical power', NULL),
(14, 'The Physician''s Cure', 'Ancient healing potion', NULL),
(15, 'Hazel''s Spatha', 'Cavalry sword made of Imperial gold', 16),
(16, 'Frank''s Spear', 'Blessed spear that transforms', 17),
(17, 'Reyna''s Cloak', 'Cloak of strength from Athena Parthenos', 18),
(18, 'Bow of Apollo', 'Golden bow with perfect accuracy', 9),
(19, 'Yankee Cap', 'Cap of invisibility from Athena', 2),
(20, 'Festus', 'Mechanical bronze dragon', 15);

-- =====================================================
-- POPULATE MAGICAL_PROPERTIES TABLE
-- =====================================================

INSERT INTO Magical_Properties (Artifact_ID, Property) VALUES
(1, 'Returns to Pocket'),
(1, 'Can Only Harm Monsters and Immortals'),
(1, 'Transforms from Pen'),
(2, 'Extremely Sharp'),
(2, 'Celestial Bronze Core'),
(3, 'Causes Panic and Fear'),
(3, 'Medusa Head Image'),
(4, 'Harms Mortals and Immortals'),
(4, 'Soul-Draining'),
(5, 'Harms Both Mortals and Monsters'),
(5, 'Cursed Blade'),
(6, 'Returns When Thrown'),
(6, 'Electric Shock'),
(7, 'Harvests Essence'),
(7, 'Time Manipulation'),
(8, 'Controls Lightning'),
(8, 'Massive Destruction'),
(9, 'Controls Water'),
(9, 'Creates Earthquakes'),
(10, 'Grants Invisibility'),
(10, 'Instills Fear'),
(11, 'Imperial Gold'),
(11, 'Kills Giants'),
(12, 'Shows Future Visions'),
(12, 'Cannot Kill'),
(13, 'Controls Mechanics'),
(13, 'Immense Power'),
(14, 'Cures Any Illness'),
(14, 'One Use Only'),
(15, 'Imperial Gold'),
(15, 'Summons Precious Metals'),
(16, 'Transforms Based on Need'),
(16, 'Blessed by Mars'),
(17, 'Grants Strength'),
(17, 'Shares Burdens'),
(18, 'Perfect Accuracy'),
(18, 'Healing Arrows'),
(19, 'Grants Invisibility'),
(20, 'Flight'),
(20, 'Fire Breath');

-- =====================================================
-- POPULATE SIGHTING_LOG TABLE
-- =====================================================

INSERT INTO Sighting_Log (Monster_ID, Sighting_Timestamp, Location, Reported_By) VALUES
(1, '2005-06-15 14:30:00', 'New York City - Empire State Building', 1),
(2, '2005-06-22 10:15:00', 'New Jersey - Aunty Em''s Garden Emporium', 1),
(3, '2005-06-28 16:45:00', 'St. Louis - Gateway Arch', 1),
(4, '2007-12-15 09:20:00', 'San Francisco Bay Area', 1),
(5, '2005-07-02 22:10:00', 'Los Angeles - DOA Recording Studios', 1),
(5, '2007-12-20 18:30:00', 'Arizona Desert', 3),
(6, '2005-06-20 11:00:00', 'New York - Greyhound Bus', 1),
(7, '2007-11-25 15:45:00', 'Maine - Westover Hall', 2),
(8, '2009-08-10 12:30:00', 'Manhattan - Empire State Building', 1),
(9, '2005-07-01 08:15:00', 'California - Waterland', 1),
(10, '2009-08-15 20:00:00', 'Manhattan Streets', 7),
(11, '2007-12-10 13:25:00', 'New Mexico Desert', 2),
(12, '2010-11-15 10:45:00', 'Alaska Wilderness', 17),
(13, '2010-07-20 14:30:00', 'Sea of Monsters - Strait', 1),
(14, '2010-07-20 14:35:00', 'Sea of Monsters - Strait', 1),
(15, '2009-08-18 12:00:00', 'Manhattan - Olympus Throne Room', 1),
(16, '2007-12-21 16:30:00', 'Mount Othrys Summit', 3),
(17, '2009-08-17 10:15:00', 'Manhattan - Chrysler Building', 1),
(18, '2009-08-16 22:45:00', 'Brooklyn Bridge', 4),
(19, '2010-10-30 19:20:00', 'Chicago Streets', 13),
(20, '2009-08-15 11:30:00', 'Manhattan - Various Locations', 6),
(21, '2005-07-03 23:55:00', 'Underworld Entrance', 1),
(22, '2009-08-17 08:00:00', 'Hudson River', 1),
(23, '2005-08-12 15:30:00', 'Delphi Ruins', 5),
(24, '2010-08-01 14:20:00', 'Tartarus', 1),
(25, '2010-06-20 12:45:00', 'Alaskan Coast', 17),
(1, '2024-05-15 16:20:00', 'Long Island Sound', 6),
(5, '2024-05-16 03:15:00', 'Camp Half-Blood Forest', 11),
(20, '2024-04-15 14:30:00', 'Queens - Subway Station', 1),
(9, '2024-06-10 10:00:00', 'Greek Countryside', 2);

-- =====================================================
-- POPULATE ENCOUNTERS TABLE
-- =====================================================

INSERT INTO Encounters (Hero_ID, Monster_ID, Encounter_Date, Location, Outcome) VALUES
(1, 1, '2005-06-15', 'Empire State Building', 'Victory'),
(1, 2, '2005-06-22', 'New Jersey', 'Victory'),
(1, 3, '2005-06-28', 'St. Louis', 'Victory'),
(1, 5, '2005-07-02', 'Los Angeles', 'Escape'),
(1, 6, '2005-06-20', 'Greyhound Bus', 'Victory'),
(1, 13, '2010-07-20', 'Sea of Monsters', 'Escape'),
(1, 14, '2010-07-20', 'Sea of Monsters', 'Escape'),
(1, 15, '2009-08-18', 'Manhattan', 'Victory'),
(2, 7, '2007-11-25', 'Maine', 'Victory'),
(2, 11, '2007-12-10', 'New Mexico', 'Victory'),
(3, 5, '2007-12-20', 'Arizona', 'Victory'),
(3, 16, '2007-12-21', 'Mount Othrys', 'Victory'),
(4, 18, '2009-08-16', 'Brooklyn Bridge', 'Victory'),
(5, 8, '2009-08-10', 'Manhattan', 'Defeat'),
(6, 20, '2009-08-15', 'Manhattan', 'Victory'),
(6, 1, '2024-05-15', 'Long Island Sound', 'Victory'),
(7, 10, '2009-08-15', 'Manhattan', 'Defeat'),
(8, 8, '2009-08-10', 'Manhattan', 'Defeat'),
(9, 23, '2005-08-12', 'Delphi', 'Victory'),
(11, 5, '2024-05-16', 'Camp Forest', 'Victory'),
(13, 19, '2010-10-30', 'Chicago', 'Victory'),
(14, 17, '2009-08-17', 'Manhattan', 'Victory'),
(15, 22, '2009-08-17', 'Hudson River', 'Escape'),
(16, 24, '2010-08-01', 'Tartarus', 'Victory'),
(17, 12, '2010-11-15', 'Alaska', 'Victory'),
(17, 25, '2010-06-20', 'Alaska', 'Victory'),
(19, 9, '2006-03-15', 'Junkyard', 'Victory'),
(20, 7, '2007-11-25', 'Maine', 'Defeat');

-- =====================================================
-- POPULATE COMBAT_ENCOUNTER TABLE
-- =====================================================

INSERT INTO Combat_Encounter (Encounter_ID, Hero_ID, Artifact_ID, Monster_ID, Quest_ID, Combat_Date, Combat_Location, Result, Notes) VALUES
(1, 1, 1, 1, 1, '2005-06-15 14:45:00', 'Empire State Building Entrance', 'Hero Victory', 'First major monster defeat for Percy'),
(2, 1, 1, 2, 1, '2005-06-22 11:30:00', 'Aunty Em''s Garden Emporium', 'Hero Victory', 'Used reflection to defeat Medusa'),
(3, 1, 1, 3, 1, '2005-06-28 17:00:00', 'Gateway Arch', 'Hero Victory', 'Chimera defeated with water'),
(4, 1, 1, 4, 1, '2005-06-30 10:15:00', 'Waterland', 'Hero Victory', 'Hydra heads cauterized'),
(5, 3, 3, 7, 2, '2007-11-25 16:00:00', 'Westover Hall', 'Hero Victory', 'Manticore driven away'),
(6, 20, NULL, 16, 2, '2007-12-21 17:00:00', 'Mount Othrys', 'Hero Victory', 'Zoe''s sacrifice'),
(7, 5, 5, 15, 3, '2009-08-18 12:30:00', 'Olympus Throne Room', 'Monster Victory', 'Luke possessed by Kronos'),
(8, 1, 1, 15, 3, '2009-08-18 13:15:00', 'Olympus Throne Room', 'Hero Victory', 'Kronos defeated'),
(9, 8, NULL, 8, 3, '2009-08-10 12:45:00', 'Princess Andromeda', 'Monster Victory', 'Beckendorf''s sacrifice'),
(10, 6, 6, 20, 3, '2009-08-15 20:30:00', 'Manhattan Streets', 'Hero Victory', 'Dracaena cleared from area'),
(11, 16, 15, 24, 4, '2010-08-01 14:45:00', 'Tartarus Depths', 'Hero Victory', 'Kampê defeated to free Death'),
(12, 1, 1, 13, 4, '2010-07-20 15:00:00', 'Sea of Monsters', 'Draw', 'Narrowly escaped'),
(13, 15, NULL, 22, 5, '2010-12-20 08:30:00', 'Athens', 'Interrupted', 'Festus damaged'),
(14, 17, 16, 25, 6, '2010-06-20 13:00:00', 'Alaskan Shore', 'Hero Victory', 'Giant defeated'),
(15, 14, 11, 17, 5, '2010-11-30 16:45:00', 'Mount Diablo', 'Hero Victory', 'Hyperion vanquished');

-- =====================================================
-- POPULATE RESCUE_MISSION TABLE
-- =====================================================

INSERT INTO Rescue_Mission (Mission_ID, Hero_ID, Quest_ID, God_Being_Rescued, Captor_Monster_ID, Mission_Date, Mission_Location, Mission_Success) VALUES
(1, 3, 2, 6, 16, '2007-12-21', 'Mount Othrys', TRUE),
(2, 14, 5, 13, NULL, '2010-10-24', 'Wolf House', TRUE),
(3, 1, 3, NULL, 15, '2009-08-18', 'Manhattan', TRUE),
(4, 16, 4, NULL, 24, '2010-08-01', 'Tartarus', TRUE);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Display summary statistics
SELECT 'Database Population Complete!' AS Status;

SELECT 'Summary Statistics:' AS '';

SELECT 'Gods' AS Entity, COUNT(*) AS Count FROM God
UNION ALL
SELECT 'Demigods', COUNT(*) FROM Demigod
UNION ALL
SELECT 'Monsters', COUNT(*) FROM Monster
UNION ALL
SELECT 'Prophecies', COUNT(*) FROM Prophecy
UNION ALL
SELECT 'Quests', COUNT(*) FROM Quest
UNION ALL
SELECT 'Divine Artifacts', COUNT(*) FROM Divine_Artifact
UNION ALL
SELECT 'Quest Logs', COUNT(*) FROM Quest_Log
UNION ALL
SELECT 'Sighting Logs', COUNT(*) FROM Sighting_Log
UNION ALL
SELECT 'Known Abilities', COUNT(*) FROM Known_Abilities
UNION ALL
SELECT 'Combat Encounters', COUNT(*) FROM Combat_Encounter
UNION ALL
SELECT 'Rescue Missions', COUNT(*) FROM Rescue_Mission;

-- =====================================================
-- END OF DATA POPULATION
-- =====================================================