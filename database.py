import sqlite3

DB_NAME = "quantro.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        country TEXT,
        wallet_address TEXT,
        kyc_status TEXT DEFAULT 'Not Submitted',
        wallet_balance REAL DEFAULT 0.0,
        affiliate_balance REAL DEFAULT 0.0,
        referrals INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def user_exists(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


def add_user(user_id, full_name, email, phone, country):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (
        user_id,
        full_name,
        email,
        phone,
        country
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        full_name,
        email,
        phone,
        country
    ))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user
