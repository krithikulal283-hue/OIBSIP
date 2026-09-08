import sqlite3
import os


DATABASE_PATH = os.path.join(
    "data",
    "bmi_records.db"
)


def create_database():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_record(
    user_name,
    weight,
    height,
    bmi,
    category,
    date_time
):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bmi_records
        (
            user_name,
            weight,
            height,
            bmi,
            category,
            date_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        weight,
        height,
        bmi,
        category,
        date_time
    ))

    connection.commit()
    connection.close()


def get_users():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT user_name
        FROM bmi_records
        ORDER BY user_name
    """)

    users = [
        row[0]
        for row in cursor.fetchall()
    ]

    connection.close()

    return users


def get_user_records(user_name):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            date_time,
            weight,
            height,
            bmi,
            category
        FROM bmi_records
        WHERE user_name = ?
        ORDER BY date_time DESC
    """, (user_name,))

    records = cursor.fetchall()

    connection.close()

    return records