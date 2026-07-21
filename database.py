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

    # =====================================
    # KYC TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kyc(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        full_name TEXT,
        id_document TEXT,
        selfie_document TEXT,
        status TEXT DEFAULT 'Pending',
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def update_wallet_address(
    user_id,
    wallet_address,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET wallet_address=?
        WHERE user_id=?
        """,
        (
            wallet_address,
            user_id,
        ),
    )

    conn.commit()
    conn.close()


def update_kyc_status(
    user_id,
    status,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET kyc_status=?
        WHERE user_id=?
        """,
        (
            status,
            user_id,
        ),
    )

    conn.commit()
    conn.close()


def update_wallet_balance(
    user_id,
    amount,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET wallet_balance=wallet_balance+?
        WHERE user_id=?
        """,
        (
            amount,
            user_id,
        ),
    )

    conn.commit()
    conn.close()
    
# =====================================
# DEPOSIT FUNCTIONS
# =====================================

def add_deposit(
    user_id,
    amount,
    tx_hash,
    status="Pending",
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO deposits(
            user_id,
            amount,
            tx_hash,
            status
        )
        VALUES(?,?,?,?)
        """,
        (
            user_id,
            amount,
            tx_hash,
            status,
        ),
    )

    conn.commit()
    conn.close()


def get_user_deposits(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM deposits
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,),
    )

    deposits = cursor.fetchall()

    conn.close()

    return deposits


# =====================================
# REFUND FUNCTIONS
# =====================================

def add_refund_request(
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

    cursor.execute(
        """
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
        """,
        (
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
        ),
    )

    conn.commit()
    conn.close()


def get_user_refunds(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM refunds
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,),
    )

    refunds = cursor.fetchall()

    conn.close()

    return refunds

# =====================================
# KYC FUNCTIONS
# =====================================

def submit_kyc(
    user_id,
    full_name,
    id_document,
    selfie_document,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO kyc(
            user_id,
            full_name,
            id_document,
            selfie_document,
            status
        )
        VALUES(?,?,?,?,?)
        """,
        (
            user_id,
            full_name,
            id_document,
            selfie_document,
            "Pending",
        ),
    )

    cursor.execute(
        """
        UPDATE users
        SET kyc_status=?
        WHERE user_id=?
        """,
        (
            "Pending",
            user_id,
        ),
    )

    conn.commit()
    conn.close()


def get_kyc(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM kyc
        WHERE user_id=?
        """,
        (user_id,),
    )

    kyc = cursor.fetchone()

    conn.close()

    return kyc


def update_kyc_status(
    user_id,
    status,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE kyc
        SET status=?
        WHERE user_id=?
        """,
        (
            status,
            user_id,
        ),
    )

    cursor.execute(
        """
        UPDATE users
        SET kyc_status=?
        WHERE user_id=?
        """,
        (
            status,
            user_id,
        ),
    )

    conn.commit()
    conn.close()
    
