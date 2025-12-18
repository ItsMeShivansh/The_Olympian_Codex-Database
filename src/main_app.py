"""
The Olympian Codex Database - Interactive Application
Team 42: RNA
Phase 4: Database Implementation

A beautiful Streamlit-based interface for managing the Greek mythology database.
"""

import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime, date
import sys

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="The Olympian Codex",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS FOR AESTHETIC STYLING
# =====================================================

def load_custom_css():
    """Apply custom CSS for a beautiful Greek mythology theme."""
    st.markdown("""
        <style>
        /* Main theme colors inspired by Greek mythology */
        :root {
            --primary-color: #DAA520;
            --secondary-color: #4B0082;
            --background-color: #0E1117;
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-header h1 {
            color: #FFD700;
            font-size: 3rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .main-header p {
            color: #FFFFFF;
            font-size: 1.2rem;
            margin-top: 0.5rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        }
        
        /* Success message styling */
        .success-message {
            padding: 1rem;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Error message styling */
        .error-message {
            padding: 1rem;
            background-color: #dc3545;
            color: white;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Card styling */
        .info-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: white;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.5rem 2rem;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #667eea;
        }
        </style>
    """, unsafe_allow_html=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

@st.cache_resource
def get_db_connection(db_user, db_pass, db_host, db_name):
    """
    Establishes a connection to the MySQL database.
    Uses Streamlit's caching to maintain connection across reruns.
    """
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return connection
    except pymysql.Error as e:
        st.error(f"❌ Error connecting to MySQL Database: {e}")
        return None

def check_connection():
    """Check if database connection exists in session state."""
    return 'db_connection' in st.session_state and st.session_state.db_connection is not None

# =====================================================
# QUERY FUNCTIONS (READ OPERATIONS)
# =====================================================

def query_demigods_by_parent(connection, god_name):
    """
    Query 1: Find all demigods by their divine parent.
    Complex query with JOIN between Demigod and God tables.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    d.Hero_ID,
                    d.First_Name,
                    d.Last_Name,
                    g.Name as Divine_Parent,
                    d.Date_of_Birth,
                    d.Fatal_Flaw,
                    d.Status
                FROM Demigod d
                JOIN God g ON d.Divine_Parent_ID = g.Divine_ID
                WHERE g.Name = %s
                ORDER BY d.First_Name
            """
            cursor.execute(sql_query, (god_name,))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_quests_with_details(connection, status=None):
    """
    Query 2: Get detailed quest information including prophecies.
    Complex query with LEFT JOIN to include quests without prophecies.
    """
    try:
        with connection.cursor() as cursor:
            if status:
                sql_query = """
                    SELECT 
                        q.Quest_ID,
                        q.Objective,
                        q.Start_Date,
                        q.End_Date,
                        q.Outcome,
                        p.Full_Text as Prophecy,
                        p.Status as Prophecy_Status
                    FROM Quest q
                    LEFT JOIN Prophecy p ON q.Prophecy_ID = p.Prophecy_ID
                    WHERE q.Outcome = %s
                    ORDER BY q.Start_Date DESC
                """
                cursor.execute(sql_query, (status,))
            else:
                sql_query = """
                    SELECT 
                        q.Quest_ID,
                        q.Objective,
                        q.Start_Date,
                        q.End_Date,
                        q.Outcome,
                        p.Full_Text as Prophecy,
                        p.Status as Prophecy_Status
                    FROM Quest q
                    LEFT JOIN Prophecy p ON q.Prophecy_ID = p.Prophecy_ID
                    ORDER BY q.Start_Date DESC
                """
                cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_monster_encounters(connection, hero_id):
    """
    Query 3: Find all monster encounters for a specific hero.
    Complex query with multiple JOINs.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    d.First_Name,
                    d.Last_Name,
                    m.Species,
                    m.Threat_Level,
                    e.Encounter_Date,
                    e.Location,
                    e.Outcome
                FROM Encounters e
                JOIN Demigod d ON e.Hero_ID = d.Hero_ID
                JOIN Monster m ON e.Monster_ID = m.Monster_ID
                WHERE d.Hero_ID = %s
                ORDER BY e.Encounter_Date DESC
            """
            cursor.execute(sql_query, (hero_id,))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_artifacts_and_wielders(connection):
    """
    Query 4: List all divine artifacts with their current wielders.
    Uses LEFT JOIN to include unwielded artifacts.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    a.Artifact_ID,
                    a.Name as Artifact_Name,
                    a.Description,
                    CONCAT(d.First_Name, ' ', d.Last_Name) as Current_Wielder,
                    GROUP_CONCAT(mp.Property SEPARATOR ', ') as Magical_Properties
                FROM Divine_Artifact a
                LEFT JOIN Demigod d ON a.Current_Wielder = d.Hero_ID
                LEFT JOIN Magical_Properties mp ON a.Artifact_ID = mp.Artifact_ID
                GROUP BY a.Artifact_ID, a.Name, a.Description, d.First_Name, d.Last_Name
                ORDER BY a.Name
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_most_dangerous_monsters(connection, min_threat_level):
    """
    Query 5: Find monsters above a certain threat level with their weaknesses.
    Complex query with aggregation and GROUP BY.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    m.Monster_ID,
                    m.Species,
                    m.Threat_Level,
                    GROUP_CONCAT(DISTINCT kw.Weakness SEPARATOR ', ') as Weaknesses,
                    GROUP_CONCAT(DISTINCT ch.Habitat SEPARATOR ', ') as Habitats,
                    COUNT(DISTINCT e.Hero_ID) as Times_Encountered
                FROM Monster m
                LEFT JOIN Known_Weaknesses kw ON m.Monster_ID = kw.Monster_ID
                LEFT JOIN Common_Habitats ch ON m.Monster_ID = ch.Monster_ID
                LEFT JOIN Encounters e ON m.Monster_ID = e.Monster_ID
                WHERE m.Threat_Level >= %s
                GROUP BY m.Monster_ID, m.Species, m.Threat_Level
                ORDER BY m.Threat_Level DESC, Times_Encountered DESC
            """
            cursor.execute(sql_query, (min_threat_level,))
            results = cursor.fetchall()
            # Convert Decimal types to int for Streamlit compatibility
            for result in results:
                result['Times_Encountered'] = int(result['Times_Encountered']) if result['Times_Encountered'] else 0
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_quest_participants(connection, quest_id):
    """
    Query 6: Get all participants of a specific quest.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    CONCAT(d.First_Name, ' ', d.Last_Name) as Hero_Name,
                    g.Name as Divine_Parent,
                    ql.Role,
                    ql.Outcome,
                    GROUP_CONCAT(ka.Ability SEPARATOR ', ') as Abilities
                FROM Quest_Log ql
                JOIN Demigod d ON ql.Hero_ID = d.Hero_ID
                LEFT JOIN God g ON d.Divine_Parent_ID = g.Divine_ID
                LEFT JOIN Known_Abilities ka ON d.Hero_ID = ka.Hero_ID
                WHERE ql.Quest_ID = %s
                GROUP BY d.Hero_ID, d.First_Name, d.Last_Name, g.Name, ql.Role, ql.Outcome
                ORDER BY ql.Role
            """
            cursor.execute(sql_query, (quest_id,))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_olympian_council(connection):
    """
    Query 7: Display the Olympian Council with seat numbers.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    o.Council_Seat_Number,
                    g.Name,
                    g.Domain,
                    g.Symbol_of_Power,
                    o.Palace_Location,
                    COUNT(DISTINCT d.Hero_ID) as Number_of_Children
                FROM Olympian o
                JOIN God g ON o.Divine_ID = g.Divine_ID
                LEFT JOIN Demigod d ON g.Divine_ID = d.Divine_Parent_ID
                WHERE o.Council_Seat_Number IS NOT NULL
                GROUP BY o.Council_Seat_Number, g.Name, g.Domain, g.Symbol_of_Power, o.Palace_Location
                ORDER BY o.Council_Seat_Number
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # Convert Decimal types to int for Streamlit compatibility
            for result in results:
                result['Number_of_Children'] = int(result['Number_of_Children']) if result['Number_of_Children'] else 0
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_active_prophecies_no_quest(connection):
    """
    REQUIRED - Selection: Retrieve all active Prophecies that have no Quest assigned.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    p.Prophecy_ID,
                    p.Full_Text,
                    p.Date_Issued,
                    p.Status
                FROM Prophecy p
                LEFT JOIN Quest q ON p.Prophecy_ID = q.Prophecy_ID
                WHERE q.Quest_ID IS NULL
                  AND p.Status != 'Fulfilled'
                  AND p.Status != 'Failed'
                ORDER BY p.Date_Issued DESC
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_demigods_projection(connection):
    """
    REQUIRED - Projection: Display the names and divine parents of all registered Demigods.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    d.First_Name,
                    d.Last_Name,
                    CONCAT(d.First_Name, ' ', d.Last_Name) as Full_Name,
                    g.Name as Divine_Parent
                FROM Demigod d
                LEFT JOIN God g ON d.Divine_Parent_ID = g.Divine_ID
                ORDER BY d.Last_Name, d.First_Name
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_titan_avg_threat(connection):
    """
    REQUIRED - Aggregate: Calculate the average Threat Level of Monsters in the Titan subclass.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    AVG(m.Threat_Level) as Average_Threat_Level,
                    COUNT(t.Monster_ID) as Total_Titans,
                    MIN(m.Threat_Level) as Min_Threat,
                    MAX(m.Threat_Level) as Max_Threat
                FROM Monster m
                JOIN Titan t ON m.Monster_ID = t.Monster_ID
            """
            cursor.execute(sql_query)
            result = cursor.fetchone()
            # Convert Decimal types to float/int for Streamlit compatibility
            if result:
                result['Average_Threat_Level'] = float(result['Average_Threat_Level']) if result['Average_Threat_Level'] else None
                result['Total_Titans'] = int(result['Total_Titans']) if result['Total_Titans'] else 0
                result['Min_Threat'] = int(result['Min_Threat']) if result['Min_Threat'] else 0
                result['Max_Threat'] = int(result['Max_Threat']) if result['Max_Threat'] else 0
            return result
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return None

def query_artifacts_search_blade(connection, search_term='Blade'):
    """
    REQUIRED - Search: Find all Divine Artifacts with a specific term in their name.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    a.Artifact_ID,
                    a.Name,
                    a.Description,
                    CONCAT(d.First_Name, ' ', d.Last_Name) as Current_Wielder,
                    GROUP_CONCAT(mp.Property SEPARATOR ', ') as Magical_Properties
                FROM Divine_Artifact a
                LEFT JOIN Demigod d ON a.Current_Wielder = d.Hero_ID
                LEFT JOIN Magical_Properties mp ON a.Artifact_ID = mp.Artifact_ID
                WHERE a.Name LIKE %s OR a.Description LIKE %s
                GROUP BY a.Artifact_ID, a.Name, a.Description, d.First_Name, d.Last_Name
                ORDER BY a.Name
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(sql_query, (search_pattern, search_pattern))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def report_quests_by_divine_parent(connection):
    """
    REQUIRED - Analysis Report 1: Generate a report of Quests grouped by the divine parent of participating Demigods.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    g.Name as Divine_Parent,
                    g.Domain,
                    COUNT(DISTINCT q.Quest_ID) as Total_Quests,
                    COUNT(DISTINCT d.Hero_ID) as Children_Participated,
                    SUM(CASE WHEN q.Outcome = 'Success' THEN 1 ELSE 0 END) as Successful_Quests,
                    GROUP_CONCAT(DISTINCT q.Objective SEPARATOR ' | ') as Quest_Objectives
                FROM God g
                JOIN Demigod d ON g.Divine_ID = d.Divine_Parent_ID
                JOIN Quest_Log ql ON d.Hero_ID = ql.Hero_ID
                JOIN Quest q ON ql.Quest_ID = q.Quest_ID
                GROUP BY g.Divine_ID, g.Name, g.Domain
                ORDER BY Total_Quests DESC, Successful_Quests DESC
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # Convert Decimal types to int for Streamlit compatibility
            for result in results:
                result['Total_Quests'] = int(result['Total_Quests']) if result['Total_Quests'] else 0
                result['Children_Participated'] = int(result['Children_Participated']) if result['Children_Participated'] else 0
                result['Successful_Quests'] = int(result['Successful_Quests']) if result['Successful_Quests'] else 0
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def report_demigod_artifact_success_rate(connection, monster_species=None):
    """
    REQUIRED - Analysis Report 2: Analyze the success rate of Demigods when using a Divine Artifact against a specific Monster species.
    """
    try:
        with connection.cursor() as cursor:
            if monster_species:
                sql_query = """
                    SELECT 
                        CONCAT(d.First_Name, ' ', d.Last_Name) as Demigod_Name,
                        a.Name as Artifact_Used,
                        m.Species as Monster_Species,
                        COUNT(*) as Total_Encounters,
                        SUM(CASE WHEN ce.Result = 'Hero Victory' THEN 1 ELSE 0 END) as Victories,
                        ROUND(SUM(CASE WHEN ce.Result = 'Hero Victory' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as Success_Rate_Percentage
                    FROM Combat_Encounter ce
                    JOIN Demigod d ON ce.Hero_ID = d.Hero_ID
                    JOIN Divine_Artifact a ON ce.Artifact_ID = a.Artifact_ID
                    JOIN Monster m ON ce.Monster_ID = m.Monster_ID
                    WHERE m.Species = %s
                    GROUP BY d.Hero_ID, d.First_Name, d.Last_Name, a.Artifact_ID, a.Name, m.Species
                    ORDER BY Success_Rate_Percentage DESC, Total_Encounters DESC
                """
                cursor.execute(sql_query, (monster_species,))
            else:
                sql_query = """
                    SELECT 
                        m.Species as Monster_Species,
                        a.Name as Artifact_Used,
                        COUNT(*) as Total_Encounters,
                        SUM(CASE WHEN ce.Result = 'Hero Victory' THEN 1 ELSE 0 END) as Victories,
                        ROUND(SUM(CASE WHEN ce.Result = 'Hero Victory' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as Success_Rate_Percentage
                    FROM Combat_Encounter ce
                    JOIN Divine_Artifact a ON ce.Artifact_ID = a.Artifact_ID
                    JOIN Monster m ON ce.Monster_ID = m.Monster_ID
                    GROUP BY m.Species, a.Artifact_ID, a.Name
                    HAVING Total_Encounters >= 1
                    ORDER BY Monster_Species, Success_Rate_Percentage DESC
                """
                cursor.execute(sql_query)
            results = cursor.fetchall()
            # Convert Decimal types to int/float for Streamlit compatibility
            for result in results:
                result['Total_Encounters'] = int(result['Total_Encounters']) if result['Total_Encounters'] else 0
                result['Victories'] = int(result['Victories']) if result['Victories'] else 0
                result['Success_Rate_Percentage'] = float(result['Success_Rate_Percentage']) if result['Success_Rate_Percentage'] else 0.0
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def report_prophecy_monster_correlation(connection):
    """
    REQUIRED - Analysis Report 3: Correlate Prophecies with the Monsters most frequently encountered in their associated Quests.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT 
                    p.Prophecy_ID,
                    LEFT(p.Full_Text, 100) as Prophecy_Text,
                    p.Status as Prophecy_Status,
                    q.Objective as Quest_Objective,
                    m.Species as Monster_Species,
                    m.Threat_Level,
                    COUNT(*) as Encounter_Count
                FROM Prophecy p
                JOIN Quest q ON p.Prophecy_ID = q.Prophecy_ID
                JOIN Combat_Encounter ce ON q.Quest_ID = ce.Quest_ID
                JOIN Monster m ON ce.Monster_ID = m.Monster_ID
                GROUP BY p.Prophecy_ID, p.Full_Text, p.Status, q.Objective, m.Species, m.Threat_Level
                ORDER BY p.Prophecy_ID, Encounter_Count DESC
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # Convert Decimal types to int for Streamlit compatibility
            for result in results:
                result['Encounter_Count'] = int(result['Encounter_Count']) if result['Encounter_Count'] else 0
            return results
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return []

def query_database_statistics(connection):
    """
    Query 8: Get overall database statistics.
    """
    try:
        with connection.cursor() as cursor:
            stats = {}
            
            # Total gods
            cursor.execute("SELECT COUNT(*) as count FROM God")
            stats['total_gods'] = cursor.fetchone()['count']
            
            # Total demigods
            cursor.execute("SELECT COUNT(*) as count FROM Demigod")
            stats['total_demigods'] = cursor.fetchone()['count']
            
            # Active demigods
            cursor.execute("SELECT COUNT(*) as count FROM Demigod WHERE Status = 'Active'")
            stats['active_demigods'] = cursor.fetchone()['count']
            
            # Total monsters
            cursor.execute("SELECT COUNT(*) as count FROM Monster")
            stats['total_monsters'] = cursor.fetchone()['count']
            
            # Total quests
            cursor.execute("SELECT COUNT(*) as count FROM Quest")
            stats['total_quests'] = cursor.fetchone()['count']
            
            # Completed quests
            cursor.execute("SELECT COUNT(*) as count FROM Quest WHERE Outcome = 'Success'")
            stats['completed_quests'] = cursor.fetchone()['count']
            
            # Total artifacts
            cursor.execute("SELECT COUNT(*) as count FROM Divine_Artifact")
            stats['total_artifacts'] = cursor.fetchone()['count']
            
            # Total encounters
            cursor.execute("SELECT COUNT(*) as count FROM Encounters")
            stats['total_encounters'] = cursor.fetchone()['count']
            
            return stats
    except pymysql.Error as e:
        st.error(f"Error during query: {e}")
        return {}

# =====================================================
# UPDATE FUNCTIONS (WRITE OPERATIONS)
# =====================================================

def insert_new_demigod(connection, first_name, last_name, divine_parent_id, date_of_birth, 
                       fatal_flaw, date_of_arrival, status, abilities=None):
    """
    REQUIRED - INSERT Operation: Add a new demigod to the database.
    The system checks that the Divine Parent exists before insertion.
    Also inserts Known_Abilities (multi-valued attribute).
    """
    try:
        with connection.cursor() as cursor:
            # First check if divine parent exists
            if divine_parent_id:
                check_sql = "SELECT Divine_ID FROM God WHERE Divine_ID = %s"
                cursor.execute(check_sql, (divine_parent_id,))
                if not cursor.fetchone():
                    return False, f"Divine Parent with ID {divine_parent_id} does not exist. Please select a valid god."
            
            # Insert demigod
            sql_insert = """
                INSERT INTO Demigod 
                (First_Name, Last_Name, Divine_Parent_ID, Date_of_Birth, Fatal_Flaw, Date_of_Arrival, Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (first_name, last_name, divine_parent_id, date_of_birth, 
                                       fatal_flaw, date_of_arrival, status))
            hero_id = cursor.lastrowid
            
            # Insert abilities if provided
            if abilities:
                for ability in abilities:
                    if ability.strip():  # Only insert non-empty abilities
                        sql_ability = "INSERT INTO Known_Abilities (Hero_ID, Ability) VALUES (%s, %s)"
                        cursor.execute(sql_ability, (hero_id, ability.strip()))
            
            connection.commit()
            return True, hero_id
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def insert_new_quest(connection, objective, start_date, outcome='Ongoing', prophecy_id=None):
    """
    INSERT Operation 2: Add a new quest.
    Links quest to a prophecy if provided (1:1 relationship).
    """
    try:
        with connection.cursor() as cursor:
            # Check if prophecy_id is provided and not already linked to another quest
            if prophecy_id:
                check_sql = "SELECT Quest_ID FROM Quest WHERE Prophecy_ID = %s"
                cursor.execute(check_sql, (prophecy_id,))
                if cursor.fetchone():
                    return False, "This prophecy is already linked to another quest."
            
            sql_insert = """
                INSERT INTO Quest (Objective, Start_Date, Outcome, Prophecy_ID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (objective, start_date, outcome, prophecy_id))
            connection.commit()
            return True, cursor.lastrowid
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def insert_monster_sighting(connection, monster_id, location, reported_by):
    """
    INSERT Operation 3: Add a new monster sighting.
    """
    try:
        with connection.cursor() as cursor:
            sighting_timestamp = datetime.now()
            sql_insert = """
                INSERT INTO Sighting_Log (Monster_ID, Sighting_Timestamp, Location, Reported_By)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (monster_id, sighting_timestamp, location, reported_by))
            connection.commit()
            return True, "Sighting recorded successfully"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def update_demigod_status(connection, hero_id, new_status):
    """
    REQUIRED - UPDATE Operation: Update a demigod's status to 'Deceased'.
    This will trigger an update on their associated 'Quest_Log' records.
    """
    try:
        with connection.cursor() as cursor:
            # Update demigod status
            sql_update = """
                UPDATE Demigod 
                SET Status = %s
                WHERE Hero_ID = %s
            """
            cursor.execute(sql_update, (new_status, hero_id))
            
            # If status is 'Deceased', update related Quest_Log entries
            if new_status == 'Deceased':
                sql_update_quest_log = """
                    UPDATE Quest_Log
                    SET Outcome = 'Deceased'
                    WHERE Hero_ID = %s AND Outcome = 'Ongoing'
                """
                cursor.execute(sql_update_quest_log, (hero_id,))
            
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Status updated successfully"
            else:
                return False, "No demigod found with that ID"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def update_quest_outcome(connection, quest_id, outcome, end_date=None):
    """
    UPDATE Operation 2: Update a quest's outcome and end date.
    """
    try:
        with connection.cursor() as cursor:
            if end_date:
                sql_update = """
                    UPDATE Quest 
                    SET Outcome = %s, End_Date = %s
                    WHERE Quest_ID = %s
                """
                cursor.execute(sql_update, (outcome, end_date, quest_id))
            else:
                sql_update = """
                    UPDATE Quest 
                    SET Outcome = %s
                    WHERE Quest_ID = %s
                """
                cursor.execute(sql_update, (outcome, quest_id))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Quest updated successfully"
            else:
                return False, "No quest found with that ID"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def update_artifact_wielder(connection, artifact_id, new_wielder_id):
    """
    UPDATE Operation 3: Change the wielder of a divine artifact.
    """
    try:
        with connection.cursor() as cursor:
            sql_update = """
                UPDATE Divine_Artifact 
                SET Current_Wielder = %s
                WHERE Artifact_ID = %s
            """
            cursor.execute(sql_update, (new_wielder_id, artifact_id))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Artifact wielder updated successfully"
            else:
                return False, "No artifact found with that ID"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def delete_monster_sighting(connection, monster_id, sighting_timestamp):
    """
    DELETE Operation 1: Remove a monster sighting record.
    """
    try:
        with connection.cursor() as cursor:
            sql_delete = """
                DELETE FROM Sighting_Log 
                WHERE Monster_ID = %s AND Sighting_Timestamp = %s
            """
            cursor.execute(sql_delete, (monster_id, sighting_timestamp))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Sighting deleted successfully"
            else:
                return False, "No sighting found with those parameters"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def delete_quest(connection, quest_id):
    """
    REQUIRED - DELETE Operation: Remove a quest record.
    All associated 'Quest_Log' entries will also be deleted due to CASCADE constraint.
    """
    try:
        with connection.cursor() as cursor:
            # Check how many quest log entries will be affected
            cursor.execute("SELECT COUNT(*) as count FROM Quest_Log WHERE Quest_ID = %s", (quest_id,))
            affected_logs = cursor.fetchone()['count']
            
            # Delete the quest (CASCADE will handle Quest_Log entries)
            sql_delete = """
                DELETE FROM Quest 
                WHERE Quest_ID = %s
            """
            cursor.execute(sql_delete, (quest_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return True, f"Quest deleted successfully. {affected_logs} quest log entries also removed due to CASCADE."
            else:
                return False, "No quest found with that ID"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

def delete_demigod_ability(connection, hero_id, ability):
    """
    DELETE Operation 3: Remove a specific ability from a demigod.
    """
    try:
        with connection.cursor() as cursor:
            sql_delete = """
                DELETE FROM Known_Abilities 
                WHERE Hero_ID = %s AND Ability = %s
            """
            cursor.execute(sql_delete, (hero_id, ability))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Ability deleted successfully"
            else:
                return False, "No such ability found for this hero"
    except pymysql.Error as e:
        connection.rollback()
        return False, str(e)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_all_gods(connection):
    """Get all gods for dropdown menus."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Divine_ID, Name FROM God ORDER BY Name")
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching gods: {e}")
        return []

def get_all_demigods(connection):
    """Get all demigods for dropdown menus."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Hero_ID, CONCAT(First_Name, ' ', Last_Name) as Full_Name 
                FROM Demigod 
                ORDER BY First_Name
            """)
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching demigods: {e}")
        return []

def get_all_monsters(connection):
    """Get all monsters for dropdown menus."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Monster_ID, Species FROM Monster ORDER BY Species")
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching monsters: {e}")
        return []

def get_all_artifacts(connection):
    """Get all artifacts for dropdown menus."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Artifact_ID, Name FROM Divine_Artifact ORDER BY Name")
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching artifacts: {e}")
        return []

def get_all_quests(connection):
    """Get all quests for dropdown menus."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Quest_ID, Objective FROM Quest ORDER BY Quest_ID DESC")
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching quests: {e}")
        return []

def get_available_prophecies(connection):
    """Get prophecies that are not yet linked to any quest."""
    try:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT p.Prophecy_ID, p.Full_Text, p.Date_Issued, p.Status
                FROM Prophecy p
                LEFT JOIN Quest q ON p.Prophecy_ID = q.Prophecy_ID
                WHERE q.Quest_ID IS NULL
                ORDER BY p.Date_Issued DESC
            """
            cursor.execute(sql_query)
            return cursor.fetchall()
    except pymysql.Error as e:
        st.error(f"Error fetching available prophecies: {e}")
        return []

# =====================================================
# UI PAGES
# =====================================================

def show_dashboard(connection):
    """Display the main dashboard with statistics."""
    st.markdown("""
        <div class="main-header">
            <h1>⚡ The Olympian Codex ⚡</h1>
            <p>A Comprehensive Database of Greek Mythology</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get statistics
    stats = query_database_statistics(connection)
    
    if stats:
        st.header("📊 Database Overview")
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏛️ Total Gods", stats['total_gods'])
            st.metric("⚔️ Total Demigods", stats['total_demigods'])
        
        with col2:
            st.metric("✅ Active Demigods", stats['active_demigods'])
            st.metric("👹 Total Monsters", stats['total_monsters'])
        
        with col3:
            st.metric("🗺️ Total Quests", stats['total_quests'])
            st.metric("🏆 Completed Quests", stats['completed_quests'])
        
        with col4:
            st.metric("⚔️ Divine Artifacts", stats['total_artifacts'])
            st.metric("⚡ Total Encounters", stats['total_encounters'])
        
        # Show Olympian Council
        st.header("🏛️ The Olympian Council")
        council_results = query_olympian_council(connection)
        if council_results:
            df = pd.DataFrame(council_results)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No council members found.")
    else:
        st.error("Unable to fetch database statistics.")

def show_query_page(connection):
    """Display the query/read operations page."""
    st.header("🔍 Query Operations")
    
    query_option = st.selectbox(
        "Select a query to execute:",
        [
            "Find Demigods by Divine Parent",
            "View Quest Details",
            # "View Monster Encounters by Hero",
            # "List Divine Artifacts",
            # "Find Dangerous Monsters",
            # "View Quest Participants",
            # "View Olympian Council",
            "Active Prophecies (No Quest Assigned)",
            "All Demigods with Divine Parents",
            "Average Threat Level of Titans",
            "Search Artifacts (Contains Text)",
            "Report: Quests by Divine Parent",
            # "Report: Demigod Success with Artifacts",
            # "Report: Prophecy-Monster Correlation"
        ]
    )
    
    st.divider()
    
    if query_option == "Find Demigods by Divine Parent":
        st.subheader("⚡ Find Demigods by Divine Parent")
        gods = get_all_gods(connection)
        if gods:
            god_names = [god['Name'] for god in gods]
            selected_god = st.selectbox("Select a god:", god_names)
            
            if st.button("🔍 Search", key="query1"):
                results = query_demigods_by_parent(connection, selected_god)
                if results:
                    st.success(f"Found {len(results)} demigod(s) with {selected_god} as their divine parent:")
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"No demigods found for {selected_god}.")
    
    elif query_option == "View Quest Details":
        st.subheader("🗺️ View Quest Details")
        status_filter = st.selectbox(
            "Filter by outcome:",
            ["All", "Success", "Failure", "Ongoing", "Abandoned"]
        )
        
        if st.button("🔍 Search", key="query2"):
            status = None if status_filter == "All" else status_filter
            results = query_quests_with_details(connection, status)
            if results:
                st.success(f"Found {len(results)} quest(s):")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No quests found.")
    
    # elif query_option == "View Monster Encounters by Hero":
    #     st.subheader("⚔️ View Monster Encounters")
    #     demigods = get_all_demigods(connection)
    #     if demigods:
    #         demigod_dict = {d['Full_Name']: d['Hero_ID'] for d in demigods}
    #         selected_demigod = st.selectbox("Select a demigod:", list(demigod_dict.keys()))
    #         
    #         if st.button("🔍 Search", key="query3"):
    #             hero_id = demigod_dict[selected_demigod]
    #             results = query_monster_encounters(connection, hero_id)
    #             if results:
    #                 st.success(f"Found {len(results)} encounter(s) for {selected_demigod}:")
    #                 df = pd.DataFrame(results)
    #                 st.dataframe(df, use_container_width=True, hide_index=True)
    #             else:
    #                 st.warning(f"No encounters found for {selected_demigod}.")
    
    # elif query_option == "List Divine Artifacts":
    #     st.subheader("⚔️ Divine Artifacts and Their Wielders")
    #     if st.button("🔍 View All Artifacts", key="query4"):
    #         results = query_artifacts_and_wielders(connection)
    #         if results:
    #             st.success(f"Found {len(results)} artifact(s):")
    #             df = pd.DataFrame(results)
    #             st.dataframe(df, use_container_width=True, hide_index=True)
    #         else:
    #             st.warning("No artifacts found.")
    
    # elif query_option == "Find Dangerous Monsters":
    #     st.subheader("👹 Find Dangerous Monsters")
    #     min_threat = st.slider("Minimum threat level:", 1, 10, 7)
    #     
    #     if st.button("🔍 Search", key="query5"):
    #         results = query_most_dangerous_monsters(connection, min_threat)
    #         if results:
    #             st.success(f"Found {len(results)} dangerous monster(s):")
    #             df = pd.DataFrame(results)
    #             st.dataframe(df, use_container_width=True, hide_index=True)
    #         else:
    #             st.warning(f"No monsters found with threat level >= {min_threat}.")
    
    # elif query_option == "View Quest Participants":
    #     st.subheader("👥 View Quest Participants")
    #     quests = get_all_quests(connection)
    #     if quests:
    #         quest_dict = {f"Quest {q['Quest_ID']}: {q['Objective'][:50]}...": q['Quest_ID'] for q in quests}
    #         selected_quest = st.selectbox("Select a quest:", list(quest_dict.keys()))
    #         
    #         if st.button("🔍 Search", key="query6"):
    #             quest_id = quest_dict[selected_quest]
    #             results = query_quest_participants(connection, quest_id)
    #             if results:
    #                 st.success(f"Found {len(results)} participant(s):")
    #                 df = pd.DataFrame(results)
    #                 st.dataframe(df, use_container_width=True, hide_index=True)
    #             else:
    #                 st.warning("No participants found for this quest.")
    
    # elif query_option == "View Olympian Council":
    #     st.subheader("🏛️ The Twelve Olympians")
    #     if st.button("🔍 View Council", key="query7"):
    #         results = query_olympian_council(connection)
    #         if results:
    #             st.success(f"The Olympian Council ({len(results)} members):")
    #             df = pd.DataFrame(results)
    #             st.dataframe(df, use_container_width=True, hide_index=True)
    #         else:
    #             st.warning("No council members found.")
    
    # ========== REQUIRED QUERIES ==========
    
    elif query_option == "Active Prophecies (No Quest Assigned)":
        st.subheader("📜 Active Prophecies with No Quest Assigned")
        st.info("**REQUIRED Query - Selection**: Retrieves all active prophecies that have no quest assigned.")
        
        if st.button("🔍 Execute Query", key="req_query1"):
            results = query_active_prophecies_no_quest(connection)
            if results:
                st.success(f"Found {len(results)} active prophecy/prophecies without assigned quests:")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("All active prophecies have quests assigned, or no active prophecies exist.")
    
    elif query_option == "All Demigods with Divine Parents":
        st.subheader("👤 All Demigods with Their Divine Parents")
        st.info("**REQUIRED Query - Projection**: Displays the names and divine parents of all registered demigods.")
        
        if st.button("🔍 Execute Query", key="req_query2"):
            results = query_demigods_projection(connection)
            if results:
                st.success(f"Found {len(results)} registered demigod(s):")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No demigods found in the database.")
    
    elif query_option == "Average Threat Level of Titans":
        st.subheader("⚡ Average Threat Level of Titans")
        st.info("**REQUIRED Query - Aggregate**: Calculates the average threat level of monsters in the Titan subclass.")
        
        if st.button("🔍 Execute Query", key="req_query3"):
            result = query_titan_avg_threat(connection)
            if result and result['Average_Threat_Level']:
                st.success("Titan Threat Level Statistics:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Average Threat", f"{result['Average_Threat_Level']:.2f}")
                with col2:
                    st.metric("Total Titans", result['Total_Titans'])
                with col3:
                    st.metric("Minimum Threat", result['Min_Threat'])
                with col4:
                    st.metric("Maximum Threat", result['Max_Threat'])
            else:
                st.warning("No Titan data found in the database.")
    
    elif query_option == "Search Artifacts (Contains Text)":
        st.subheader("🔍 Search Divine Artifacts")
        st.info("**REQUIRED Query - Search**: Find all divine artifacts with specific text in their name or description.")
        
        search_term = st.text_input("Enter search term (e.g., 'Blade', 'Sword', 'Shield'):", value="Blade")
        
        if st.button("🔍 Execute Search", key="req_query4"):
            if search_term:
                results = query_artifacts_search_blade(connection, search_term)
                if results:
                    st.success(f"Found {len(results)} artifact(s) matching '{search_term}':")
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"No artifacts found matching '{search_term}'.")
            else:
                st.warning("Please enter a search term.")
    
    # ========== ANALYSIS REPORTS ==========
    
    elif query_option == "Report: Quests by Divine Parent":
        st.subheader("📊 Analysis Report: Quests by Divine Parent")
        st.info("**REQUIRED Report 1**: Generates a report of quests grouped by the divine parent of participating demigods.")
        
        if st.button("📊 Generate Report", key="report1"):
            results = report_quests_by_divine_parent(connection)
            if results:
                st.success(f"Report generated for {len(results)} divine parent(s):")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Summary statistics
                st.subheader("Summary Statistics")
                total_quests = sum(r['Total_Quests'] for r in results)
                total_successful = sum(r['Successful_Quests'] for r in results)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Quests Across All Parents", total_quests)
                with col2:
                    st.metric("Total Successful Quests", total_successful)
            else:
                st.warning("No quest data found.")
    
    # elif query_option == "Report: Demigod Success with Artifacts":
    #     st.subheader("📊 Analysis Report: Demigod Success Rate with Artifacts")
    #     st.info("**REQUIRED Report 2**: Analyzes the success rate of demigods when using divine artifacts against specific monster species.")
    #     
    #     monsters = get_all_monsters(connection)
    #     if monsters:
    #         monster_species = ["All Species"] + sorted(list(set([m['Species'] for m in monsters])))
    #         selected_species = st.selectbox("Filter by Monster Species:", monster_species)
    #         
    #         if st.button("📊 Generate Report", key="report2"):
    #             species = None if selected_species == "All Species" else selected_species
    #             results = report_demigod_artifact_success_rate(connection, species)
    #             if results:
    #                 st.success(f"Report generated for {len(results)} encounter(s):")
    #                 df = pd.DataFrame(results)
    #                 st.dataframe(df, use_container_width=True, hide_index=True)
    #             else:
    #                 st.warning("No combat encounter data found with artifacts.")
    
    # elif query_option == "Report: Prophecy-Monster Correlation":
    #     st.subheader("📊 Analysis Report: Prophecy-Monster Correlation")
    #     st.info("**REQUIRED Report 3**: Correlates prophecies with the monsters most frequently encountered in their associated quests.")
    #     
    #     if st.button("📊 Generate Report", key="report3"):
    #         results = report_prophecy_monster_correlation(connection)
    #         if results:
    #             st.success(f"Report generated for {len(results)} prophecy-monster correlation(s):")
    #             df = pd.DataFrame(results)
    #             st.dataframe(df, use_container_width=True, hide_index=True)
    #         else:
    #             st.warning("No prophecy-quest-monster correlations found.")

def show_insert_page(connection):
    """Display the insert operations page."""
    st.header("➕ Insert Operations")
    
    insert_option = st.selectbox(
        "Select an insert operation:",
        [
            "Add New Demigod",
            "Create New Quest",
            "Report Monster Sighting"
        ]
    )
    
    st.divider()
    
    if insert_option == "Add New Demigod":
        st.subheader("⚔️ Register a New Demigod")
        # st.info("**REQUIRED Insert**: The system checks that the Divine Parent exists before insertion.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name:")
            last_name = st.text_input("Last Name:")
            
            gods = get_all_gods(connection)
            if gods:
                god_dict = {g['Name']: g['Divine_ID'] for g in gods}
                selected_god = st.selectbox("Divine Parent:", ["None"] + list(god_dict.keys()))
                divine_parent_id = None if selected_god == "None" else god_dict[selected_god]
        
        with col2:
            date_of_birth = st.date_input("Date of Birth:", value=date(2000, 1, 1))
            date_of_arrival = st.date_input("Date of Arrival at Camp:", value=date.today())
            fatal_flaw = st.text_input("Fatal Flaw:")
            status = st.selectbox("Status:", ["Active", "Deceased", "Missing", "Retired"])
        
        # Multi-valued attribute: Known Abilities
        st.subheader("Known Abilities (Optional)")
        abilities_text = st.text_area(
            "Enter abilities (one per line):",
            placeholder="Water Manipulation\nUnderwater Breathing\nSwordsmanship",
            height=100
        )
        
        if st.button("✅ Register Demigod", key="insert1"):
            if first_name and last_name and fatal_flaw:
                # Parse abilities from text area
                abilities = [ability.strip() for ability in abilities_text.split('\n') if ability.strip()]
                
                success, result = insert_new_demigod(
                    connection, first_name, last_name, divine_parent_id,
                    date_of_birth, fatal_flaw, date_of_arrival, status, abilities
                )
                if success:
                    st.success(f"✅ Demigod registered successfully! Hero ID: {result}")
                    if abilities:
                        st.info(f"📋 Added {len(abilities)} ability/abilities.")
                else:
                    st.error(f"❌ Error: {result}")
            else:
                st.warning("Please fill in all required fields.")
    
    elif insert_option == "Create New Quest":
        st.subheader("🗺️ Create a New Quest")
        
        objective = st.text_area("Quest Objective:", height=100)
        start_date = st.date_input("Start Date:", value=date.today())
        outcome = st.selectbox("Initial Outcome:", ["Ongoing", "Success", "Failure", "Abandoned"])
        
        # Link to Prophecy (1:1 relationship)
        st.subheader("Link to Prophecy (Optional)")
        available_prophecies = get_available_prophecies(connection)
        
        prophecy_id = None
        if available_prophecies:
            prophecy_options = ["None - No Prophecy"] + [
                f"Prophecy {p['Prophecy_ID']}: {p['Full_Text'][:80]}..." 
                for p in available_prophecies
            ]
            selected_prophecy = st.selectbox("Select a Prophecy:", prophecy_options)
            
            if selected_prophecy != "None - No Prophecy":
                # Extract prophecy_id from selection
                prophecy_id = available_prophecies[prophecy_options.index(selected_prophecy) - 1]['Prophecy_ID']
                
                # Show full prophecy text
                selected_prophecy_data = available_prophecies[prophecy_options.index(selected_prophecy) - 1]
                st.info(f"**Full Prophecy Text:**\n{selected_prophecy_data['Full_Text']}")
        else:
            st.warning("⚠️ No available prophecies. All prophecies are already linked to quests.")
        
        if st.button("✅ Create Quest", key="insert2"):
            if objective:
                success, result = insert_new_quest(connection, objective, start_date, outcome, prophecy_id)
                if success:
                    st.success(f"✅ Quest created successfully! Quest ID: {result}")
                    if prophecy_id:
                        st.info(f"🔗 Quest linked to Prophecy ID: {prophecy_id}")
                else:
                    st.error(f"❌ Error: {result}")
            else:
                st.warning("Please provide a quest objective.")
    
    elif insert_option == "Report Monster Sighting":
        st.subheader("👁️ Report a Monster Sighting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monsters = get_all_monsters(connection)
            if monsters:
                monster_dict = {m['Species']: m['Monster_ID'] for m in monsters}
                selected_monster = st.selectbox("Monster Species:", list(monster_dict.keys()))
                monster_id = monster_dict[selected_monster]
        
        with col2:
            demigods = get_all_demigods(connection)
            if demigods:
                demigod_dict = {d['Full_Name']: d['Hero_ID'] for d in demigods}
                selected_reporter = st.selectbox("Reported By:", list(demigod_dict.keys()))
                reporter_id = demigod_dict[selected_reporter]
        
        location = st.text_input("Location:")
        
        if st.button("✅ Report Sighting", key="insert3"):
            if location:
                success, result = insert_monster_sighting(connection, monster_id, location, reporter_id)
                if success:
                    st.success(f"✅ Sighting reported successfully!")
                else:
                    st.error(f"❌ Error: {result}")
            else:
                st.warning("Please provide a location.")

def show_update_page(connection):
    """Display the update operations page."""
    st.header("✏️ Update Operations")
    
    update_option = st.selectbox(
        "Select an update operation:",
        [
            "Update Demigod Status",
            "Update Quest Outcome",
            "Change Artifact Wielder"
        ]
    )
    
    st.divider()
    
    if update_option == "Update Demigod Status":
        st.subheader("✏️ Update Demigod Status")
        st.info("**REQUIRED Update**: When updating to 'Deceased', this triggers an update on associated 'Quest_Log' records.")
        
        demigods = get_all_demigods(connection)
        if demigods:
            demigod_dict = {d['Full_Name']: d['Hero_ID'] for d in demigods}
            selected_demigod = st.selectbox("Select Demigod:", list(demigod_dict.keys()))
            hero_id = demigod_dict[selected_demigod]
            
            new_status = st.selectbox("New Status:", ["Active", "Deceased", "Missing", "Retired"])
            
            if new_status == "Deceased":
                st.warning("⚠️ Updating to 'Deceased' will also update all ongoing Quest_Log entries for this hero.")
            
            if st.button("✅ Update Status", key="update1"):
                success, result = update_demigod_status(connection, hero_id, new_status)
                if success:
                    st.success(f"✅ {result}")
                else:
                    st.error(f"❌ Error: {result}")
    
    elif update_option == "Update Quest Outcome":
        st.subheader("✏️ Update Quest Outcome")
        
        quests = get_all_quests(connection)
        if quests:
            quest_dict = {f"Quest {q['Quest_ID']}: {q['Objective'][:50]}...": q['Quest_ID'] for q in quests}
            selected_quest = st.selectbox("Select Quest:", list(quest_dict.keys()))
            quest_id = quest_dict[selected_quest]
            
            outcome = st.selectbox("New Outcome:", ["Success", "Failure", "Ongoing", "Abandoned"])
            
            set_end_date = st.checkbox("Set End Date")
            end_date = None
            if set_end_date:
                end_date = st.date_input("End Date:", value=date.today())
            
            if st.button("✅ Update Quest", key="update2"):
                success, result = update_quest_outcome(connection, quest_id, outcome, end_date)
                if success:
                    st.success(f"✅ {result}")
                else:
                    st.error(f"❌ Error: {result}")
    
    elif update_option == "Change Artifact Wielder":
        st.subheader("⚔️ Change Artifact Wielder")
        
        artifacts = get_all_artifacts(connection)
        demigods = get_all_demigods(connection)
        
        if artifacts and demigods:
            artifact_dict = {a['Name']: a['Artifact_ID'] for a in artifacts}
            selected_artifact = st.selectbox("Select Artifact:", list(artifact_dict.keys()))
            artifact_id = artifact_dict[selected_artifact]
            
            demigod_dict = {d['Full_Name']: d['Hero_ID'] for d in demigods}
            selected_wielder = st.selectbox("New Wielder:", ["None"] + list(demigod_dict.keys()))
            new_wielder_id = None if selected_wielder == "None" else demigod_dict[selected_wielder]
            
            if st.button("✅ Change Wielder", key="update3"):
                success, result = update_artifact_wielder(connection, artifact_id, new_wielder_id)
                if success:
                    st.success(f"✅ {result}")
                else:
                    st.error(f"❌ Error: {result}")

def show_delete_page(connection):
    """Display the delete operations page."""
    st.header("🗑️ Delete Operations")
    
    st.warning("⚠️ Warning: Delete operations are permanent and cannot be undone!")
    
    delete_option = st.selectbox(
        "Select a delete operation:",
        [
            "Delete Monster Sighting",
            "Delete Quest",
            "Remove Demigod Ability"
        ]
    )
    
    st.divider()
    
    if delete_option == "Delete Monster Sighting":
        st.subheader("🗑️ Delete a Monster Sighting")
        
        # Get recent sightings
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        sl.Monster_ID,
                        m.Species,
                        sl.Sighting_Timestamp,
                        sl.Location,
                        CONCAT(d.First_Name, ' ', d.Last_Name) as Reporter
                    FROM Sighting_Log sl
                    JOIN Monster m ON sl.Monster_ID = m.Monster_ID
                    LEFT JOIN Demigod d ON sl.Reported_By = d.Hero_ID
                    ORDER BY sl.Sighting_Timestamp DESC
                    LIMIT 20
                """)
                sightings = cursor.fetchall()
                
                if sightings:
                    df = pd.DataFrame(sightings)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    sighting_dict = {
                        f"{s['Species']} at {s['Location']} ({s['Sighting_Timestamp']})": 
                        (s['Monster_ID'], s['Sighting_Timestamp']) 
                        for s in sightings
                    }
                    
                    selected_sighting = st.selectbox("Select Sighting to Delete:", list(sighting_dict.keys()))
                    
                    if st.button("🗑️ Delete Sighting", key="delete1"):
                        monster_id, timestamp = sighting_dict[selected_sighting]
                        success, result = delete_monster_sighting(connection, monster_id, timestamp)
                        if success:
                            st.success(f"✅ {result}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
                else:
                    st.info("No sightings found.")
        except pymysql.Error as e:
            st.error(f"Error fetching sightings: {e}")
    
    elif delete_option == "Delete Quest":
        st.subheader("🗑️ Delete a Quest")
        st.info("**REQUIRED Delete**: All associated 'Quest_Log' entries will also be deleted due to CASCADE constraint.")
        
        quests = get_all_quests(connection)
        if quests:
            quest_dict = {f"Quest {q['Quest_ID']}: {q['Objective'][:50]}...": q['Quest_ID'] for q in quests}
            selected_quest = st.selectbox("Select Quest to Delete:", list(quest_dict.keys()))
            quest_id = quest_dict[selected_quest]
            
            st.warning("⚠️ This will CASCADE delete all quest logs associated with this quest!")
            
            confirm = st.checkbox("I understand this action is permanent")
            
            if st.button("🗑️ Delete Quest", key="delete2", disabled=not confirm):
                success, result = delete_quest(connection, quest_id)
                if success:
                    st.success(f"✅ {result}")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result}")
    
    elif delete_option == "Remove Demigod Ability":
        st.subheader("🗑️ Remove a Demigod Ability")
        
        demigods = get_all_demigods(connection)
        if demigods:
            demigod_dict = {d['Full_Name']: d['Hero_ID'] for d in demigods}
            selected_demigod = st.selectbox("Select Demigod:", list(demigod_dict.keys()))
            hero_id = demigod_dict[selected_demigod]
            
            # Get abilities for selected demigod
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT Ability FROM Known_Abilities 
                        WHERE Hero_ID = %s
                        ORDER BY Ability
                    """, (hero_id,))
                    abilities = cursor.fetchall()
                    
                    if abilities:
                        ability_list = [a['Ability'] for a in abilities]
                        selected_ability = st.selectbox("Select Ability to Remove:", ability_list)
                        
                        if st.button("🗑️ Remove Ability", key="delete3"):
                            success, result = delete_demigod_ability(connection, hero_id, selected_ability)
                            if success:
                                st.success(f"✅ {result}")
                                st.rerun()
                            else:
                                st.error(f"❌ Error: {result}")
                    else:
                        st.info(f"No abilities found for {selected_demigod}.")
            except pymysql.Error as e:
                st.error(f"Error fetching abilities: {e}")

def show_about_page():
    """Display the about page."""
    st.header("ℹ️ About The Olympian Codex")
    
    st.markdown("""
    ### 🏛️ Welcome to The Olympian Codex
    
    This is a comprehensive database management system for Greek mythology, featuring:
    
    - **Gods & Goddesses**: The mighty Olympians, chthonic deities, and primordials
    - **Demigods**: Heroic half-bloods with divine parentage
    - **Monsters**: Fearsome creatures and threats from mythology
    - **Quests**: Epic adventures guided by prophecies
    - **Divine Artifacts**: Powerful weapons and magical items
    
    ### 📊 Database Features
    
    #### Query Operations (Read)
    - Find demigods by their divine parent
    - View detailed quest information with prophecies
    - Track monster encounters by hero
    - List divine artifacts and their wielders
    - Identify the most dangerous monsters
    - View quest participants and their roles
    - Display the Olympian Council
    
    #### Insert Operations (Create)
    - Register new demigods
    - Create new quests
    - Report monster sightings
    
    #### Update Operations (Modify)
    - Update demigod status
    - Change quest outcomes
    - Transfer artifact ownership
    
    #### Delete Operations (Remove)
    - Delete monster sightings
    - Remove quests
    - Remove demigod abilities
    
    ### 👥 Team Information
    
    **Team 42: RNA**  
    **Phase 4: Database Implementation**
    
    ### 🛠️ Technical Stack
    
    - **Database**: MySQL
    - **Backend**: Python with PyMySQL
    - **Frontend**: Streamlit
    - **Design**: Entity-Relationship Model with proper normalization
    
    ### 📜 Database Schema Highlights
    
    - Strong entities with proper primary keys
    - Foreign key relationships with referential integrity
    - Subclass hierarchies (Olympian, Chthonic God, Primordial)
    - Weak entities (Quest_Log, Sighting_Log)
    - Multi-valued attributes handled through separate tables
    - Complex many-to-many relationships
    
    ---
    
    *May the gods be with you on your database journey!* ⚡
    """)

# =====================================================
# MAIN APPLICATION
# =====================================================

def main():
    """Main application entry point."""
    
    # Apply custom CSS
    load_custom_css()
    
    # Initialize session state
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = None
    
    # Sidebar for database connection
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/lightning-bolt.png", width=100)
        st.title("⚡ The Olympian Codex")
        st.divider()
        
        if not check_connection():
            st.header("🔐 Database Connection")
            
            db_host = st.text_input("Host:", value="localhost")
            db_name = st.text_input("Database:", value="olympian_codex_db")
            db_user = st.text_input("Username:", value="root")
            db_pass = st.text_input("Password:", type="password")
            
            if st.button("🔌 Connect", use_container_width=True):
                connection = get_db_connection(db_user, db_pass, db_host, db_name)
                if connection:
                    st.session_state.db_connection = connection
                    st.success("✅ Connected successfully!")
                    st.rerun()
                else:
                    st.error("❌ Connection failed!")
        else:
            st.success("✅ Database Connected")
            
            if st.button("🔌 Disconnect", use_container_width=True):
                if st.session_state.db_connection:
                    st.session_state.db_connection.close()
                st.session_state.db_connection = None
                st.rerun()
            
            st.divider()
            
            # Navigation menu
            st.header("📑 Navigation")
            page = st.radio(
                "Select a page:",
                [
                    "🏠 Dashboard",
                    "🔍 Query Operations",
                    "➕ Insert Operations",
                    "✏️ Update Operations",
                    "🗑️ Delete Operations",
                    "ℹ️ About"
                ],
                label_visibility="collapsed"
            )
            
            st.divider()
            st.caption("Team 42: RNA | Phase 4")
    
    # Main content area
    if not check_connection():
        st.markdown("""
            <div class="main-header">
                <h1>⚡ The Olympian Codex ⚡</h1>
                <p>A Comprehensive Database of Greek Mythology</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("👈 Please connect to the database using the sidebar to begin.")
        
        # Display welcome information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="info-card">
                    <h3>🏛️ Gods & Demigods</h3>
                    <p>Explore the divine pantheon and their heroic children</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="info-card">
                    <h3>👹 Monsters & Quests</h3>
                    <p>Track legendary creatures and epic adventures</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="info-card">
                    <h3>⚔️ Divine Artifacts</h3>
                    <p>Manage powerful weapons and magical items</p>
                </div>
            """, unsafe_allow_html=True)
        
    else:
        # Route to appropriate page
        connection = st.session_state.db_connection
        
        if page == "🏠 Dashboard":
            show_dashboard(connection)
        elif page == "🔍 Query Operations":
            show_query_page(connection)
        elif page == "➕ Insert Operations":
            show_insert_page(connection)
        elif page == "✏️ Update Operations":
            show_update_page(connection)
        elif page == "🗑️ Delete Operations":
            show_delete_page(connection)
        elif page == "ℹ️ About":
            show_about_page()

if __name__ == "__main__":
    main()
