import sqlite3

# Connect to database file (it will create it if it doesn't exist)
conn = sqlite3.connect("resume_checker.db")
cursor = conn.cursor()

# Create table for storing candidate evaluations
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    jd_role TEXT,
    resume_text TEXT,
    jd_text TEXT,
    score REAL,
    verdict TEXT,
    missing_skills TEXT,
    improvement_suggestions TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database created and table ready!")
