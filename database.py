import sqlite3

def create_table():

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        location TEXT,
        program_area TEXT,
        stakeholders TEXT,
        notes TEXT,
        debrief TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_report(
    date,
    location,
    program_area,
    stakeholders,
    notes,
    debrief
):

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports
    (
        date,
        location,
        program_area,
        stakeholders,
        notes,
        debrief
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        str(date),
        location,
        program_area,
        stakeholders,
        notes,
        debrief
    ))

    conn.commit()
    conn.close()