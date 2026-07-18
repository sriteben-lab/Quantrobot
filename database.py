import sqlite3

DB_NAME = "quantro.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
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

# Add referral columns if they don't already exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN referrer_id INTEGER")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN first_deposit INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass

# Deposits Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS deposits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    network TEXT,
    amount REAL,
    crypto_amount REAL,
    txid TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

    # Add crypto_amount column if it doesn't exist
    try:
        cursor.execute(
            "ALTER TABLE deposits ADD COLUMN crypto_amount REAL"
        )
    except sqlite3.OperationalError:
        pass

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


def add_deposit(user_id, network, usd_amount, crypto_amount, txid):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO deposits(
        user_id,
        network,
        amount,
        crypto_amount,
        txid
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        network,
        usd_amount,
        crypto_amount,
        txid
    ))

    conn.commit()
    conn.close()


def get_pending_deposits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            network,
            amount,
            crypto_amount,
            txid,
            status
        FROM deposits
        WHERE status='Pending'
    """)

    deposits = cursor.fetchall()

    conn.close()

    return deposits


def get_user_deposits(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            network,
            amount,
            crypto_amount,
            txid,
            status
        FROM deposits
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    deposits = cursor.fetchall()

    conn.close()

    return deposits
    def get_user_deposits(user_id):
    ...
    return deposits


# ==============================
# REFERRAL FUNCTIONS
# ==============================

def set_referrer(user_id, referrer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET referrer_id=?
        WHERE user_id=?
    """, (referrer_id, user_id))

    conn.commit()
    conn.close()


def get_referrer(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT referrer_id
        FROM users
        WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None


def increment_referrals(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET referrals = referrals + 1
        WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()


def add_affiliate_balance(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET affiliate_balance = affiliate_balance + ?
        WHERE user_id=?
    """, (amount, user_id))

    conn.commit()
    conn.close()
