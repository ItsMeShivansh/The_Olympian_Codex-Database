# The Olympian Codex Database

> A comprehensive MySQL database management system for Greek mythology featuring gods, demigods, monsters, quests, and divine artifacts.

[![Demo Video](https://img.shields.io/badge/Demo-Video-blue)](https://drive.google.com/file/d/18kkcPyJkcgyuMxAqAfyF7E_Q3wACcIea/view?usp=sharing)

## 🎯 Project Overview

A full-stack database application that models the complex relationships and hierarchies of Greek mythology. Built with MySQL and Python, this system demonstrates advanced database design concepts including multi-valued attributes, weak entities, subclass hierarchies, and referential integrity constraints. Features a user-friendly Streamlit interface for performing CRUD operations and running complex analytical queries.

---

## 🚀 Quick Start

### Prerequisites
- MySQL 8.0+
- Python 3.8+
- Required Python packages: `streamlit`, `pymysql`, `pandas`

### Installation
```bash
# Install dependencies
pip install streamlit pymysql pandas

# Set up database
mysql -u root -p < schema.sql
mysql -u root -p < populate.sql

# Launch application
streamlit run main_app.py
```

---

## 📊 Database Features

### Query Operations (7 Active Queries)

#### **1. Find Demigods by Divine Parent**
- **Type**: Selection with JOIN
- **Purpose**: Lists all demigods for a specific god/goddess
- **Returns**: Hero details, divine parent, date of birth, fatal flaw, status

#### **2. View Quest Details**
- **Type**: Complex JOIN with filtering
- **Purpose**: Shows quests with linked prophecies
- **Filters**: Success, Failure, Ongoing, Abandoned, or All
- **Returns**: Quest objective, dates, outcome, prophecy text

#### **3. Active Prophecies (No Quest Assigned)** 
- **Type**: Selection with LEFT JOIN
- **Purpose**: Finds prophecies awaiting quest assignment
- **Returns**: Prophecy ID, full text, date issued, status

#### **4. All Demigods with Divine Parents** 
- **Type**: Projection query
- **Purpose**: Simple listing of all registered demigods
- **Returns**: First name, last name, divine parent name

#### **5. Average Threat Level of Titans** 
- **Type**: Aggregate query
- **Purpose**: Statistical analysis of Titan monsters
- **Returns**: AVG, MIN, MAX threat levels, total count

#### **6. Search Artifacts (Contains Text)** 
- **Type**: Search query with LIKE operator
- **Purpose**: Finds artifacts by name/description keywords
- **Returns**: Artifact details, wielder, magical properties

#### **7. Report: Quests by Divine Parent** 
- **Type**: Complex analysis report with GROUP BY
- **Purpose**: Aggregates quest participation by divine lineage
- **Returns**: Total quests, successful quests, children participated per god

---

### Insert Operations (3 Operations)

#### **1. Add New Demigod** 
- Validates divine parent existence before insertion
- Supports multi-valued `Known_Abilities` attribute
- Auto-generates Hero_ID

#### **2. Create New Quest** 
- Links quest to available prophecy (1:1 relationship)
- Prevents duplicate prophecy assignments
- Sets initial outcome status

#### **3. Report Monster Sighting**
- Records timestamp, location, and reporter
- Creates weak entity record in `Sighting_Log`

---

### Update Operations (3 Operations)

#### **1. Update Demigod Status** 
- Updates demigod status (Active/Deceased/Missing/Retired)
- **CASCADE Effect**: Sets `Quest_Log.Outcome = 'Deceased'` for ongoing quests when status = 'Deceased'

#### **2. Update Quest Outcome**
- Changes quest result (Success/Failure/Ongoing/Abandoned)
- Optionally sets end date

#### **3. Change Artifact Wielder**
- Transfers divine artifact to new demigod
- Supports unwielding (set to NULL)

---

### Delete Operations (3 Operations)

#### **1. Delete Monster Sighting**
- Removes specific `Sighting_Log` entry
- Uses composite key (Monster_ID, Sighting_Timestamp)

#### **2. Delete Quest** 
- Deletes quest record
- **CASCADE Effect**: Automatically removes all `Quest_Log` entries due to ON DELETE CASCADE constraint
- Shows count of affected quest log records

#### **3. Remove Demigod Ability**
- Deletes specific ability from `Known_Abilities` table
- Uses composite key (Hero_ID, Ability)

---

## 🗄️ Database Schema Overview

### Strong Entities
- **God** (20 records): Divine entities with domains and symbols
- **Demigod** (25 records): Half-blood heroes with fatal flaws
- **Monster** (25 records): Mythological threats with threat levels
- **Prophecy** (10 records): Oracle predictions
- **Quest** (12 records): Heroic missions
- **Divine_Artifact** (20 records): Magical weapons and items

### Subclass Hierarchies
- **Gods**: Olympian, Chthonic_God, Primordial
- **Monsters**: Beast, Titan, Spirit

### Weak Entities
- **Quest_Log**: Demigod participation in quests
- **Sighting_Log**: Monster sighting records

### Multi-valued Attributes
- **Known_Abilities**: Demigod powers
- **Known_Weaknesses**: Monster vulnerabilities
- **Common_Habitats**: Monster locations
- **Magical_Properties**: Artifact enchantments

### Relationships
- **Encounters** (M:N): Hero vs Monster combat records
- **Combat_Encounter**: Complex combat events with artifacts and quests
- **Rescue_Mission**: God rescue operations

---

## 🔑 Key Design Features

**Referential Integrity**: Foreign keys with CASCADE/SET NULL constraints  
**Insertion Anomaly Prevention**: Nullable Divine_Parent_ID in Demigod  
**Deletion Anomaly Prevention**: SET NULL on god deletion  
**Multi-valued Attributes**: Separate tables with composite keys  
**Subclass Implementation**: Shared primary keys with parent entities  
**Weak Entity Support**: Composite keys dependent on strong entities  
**Data Validation**: CHECK constraints and ENUM types  

---

## 🛠️ Technical Stack

- **Database**: MySQL 8.0+ with InnoDB engine
- **Backend**: Python 3.8+ with PyMySQL connector
- **Frontend**: Streamlit web framework
- **Data Handling**: Pandas for DataFrames
- **Query Style**: Raw SQL with parameterized queries (no ORM)

---

## 💡 Key Achievements

- ✅ Implemented **16 different database operations** (7 queries, 3 inserts, 3 updates, 3 deletes)
- ✅ Modeled **125+ records** across 6 strong entities and multiple supporting tables
- ✅ Designed complex relationships including M:N associations and weak entities
- ✅ Applied CASCADE constraints for automatic referential integrity maintenance
- ✅ Built intuitive web interface for non-technical users
- ✅ Prevented SQL injection through parameterized queries

---

## 📂 Repository Structure

```
├── src/
│   ├── schema.sql      # Database schema with constraints
│   ├── populate.sql    # Sample data (125+ records)
│   └── main_app.py     # Streamlit application
├── README.md
└── Demo_Video_Link.txt
```

---

## 📝 Notes

- All queries use parameterized SQL for injection prevention
- Decimal type conversions implemented for Streamlit compatibility
- CASCADE constraints handle referential integrity automatically
- Multi-valued attributes properly normalized into separate tables
- 1:1 relationship enforced between Quest and Prophecy via UNIQUE constraint

---

*May the gods be with you on your database journey!* ⚡

---

**Author**: [ItsMeShivansh](https://github.com/ItsMeShivansh)  
**Project**: The Olympian Codex Database  
**Year**: 2025
