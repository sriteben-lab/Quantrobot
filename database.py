import sqlite3

DB_NAME = "quantro.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # USERS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
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

    # Add referral columns if upgrading an old database
    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN referrer_id INTEGER"
        )
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN first_deposit INTEGER DEFAULT 0"
        )
    except sqlite3.OperationalError:
        pass

    # =====================================
    # DEPOSITS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        network TEXT,
        amount REAL,
        crypto_amount REAL,
        txid TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # =====================================
    # REFUND REQUESTS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refunds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        full_name TEXT,

        investment_date TEXT,

        profile_id TEXT,

        investment_amount TEXT,

        cryptocurrency TEXT,

        exchange_wallet TEXT,

        sender_wallet TEXT,

        evidence_text TEXT,

        evidence_file_ids TEXT,

        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# USER FUNCTIONS
# =====================================

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


def add_user(
    user_id,
    full_name,
    email,
    phone,
    country,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(
        user_id,
        full_name,
        email,
        phone,
        country
    )
    VALUES(?,?,?,?,?)
    """, (
        user_id,
        full_name,
        email,
        phone,
        country,
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
  # =====================================
# DEPOSIT FUNCTIONS
# =====================================

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
    VALUES(?,?,?,?,?)
    """, (
        user_id,
        network,
        usd_amount,
        crypto_amount,
        txid,
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
    ORDER BY id DESC
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

# =====================================
# REFUND FUNCTIONS
# =====================================

def add_refund(
    user_id,
    full_name,
    investment_date,
    profile_id,
    investment_amount,
    cryptocurrency,
    exchange_wallet,
    sender_wallet,
    evidence_text,
    evidence_file_ids,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO refunds(
        user_id,
        full_name,
        investment_date,
        profile_id,
        investment_amount,
        cryptocurrency,
        exchange_wallet,
        sender_wallet,
        evidence_text,
        evidence_file_ids
    )
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """, (
        user_id,
        full_name,
        investment_date,
        profile_id,
        investment_amount,
        cryptocurrency,
        exchange_wallet,
        sender_wallet,
        evidence_text,
        evidence_file_ids,
    ))

    conn.commit()
    conn.close()


def get_pending_refunds():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM refunds
    WHERE status='Pending'
    ORDER BY id DESC
    """)

    refunds = cursor.fetchall()

    conn.close()

    return refunds


def get_user_refunds(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        investment_date,
        investment_amount,
        cryptocurrency,
        status
    FROM refunds
    WHERE user_id=?
    ORDER BY id DESC
    """, (user_id,))

    refunds = cursor.fetchall()

    conn.close()

    return refunds


def get_refund(refund_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM refunds
    WHERE id=?
    """, (refund_id,))

    refund = cursor.fetchone()

    conn.close()

    return refund


def update_refund_status(refund_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE refunds
    SET status=?
    WHERE id=?
    """, (
        status,
        refund_id,
    ))

    conn.commit()
    conn.close()
  
# =====================================
# REFERRAL FUNCTIONS
# =====================================

def set_referrer(user_id, referrer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET referrer_id=?
    WHERE user_id=?
    """, (
        referrer_id,
        user_id,
    ))

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
    """, (
        amount,
        user_id,
    ))

    conn.commit()
    conn.close()


# =====================================
# WALLET FUNCTIONS
# =====================================

def get_wallet_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT wallet_balance
    FROM users
    WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0.0


def update_wallet_balance(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET wallet_balance=?
   
