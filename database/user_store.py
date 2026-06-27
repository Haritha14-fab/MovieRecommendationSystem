"""SQLite user persistence."""

import logging
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from config import Config

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    """Open a connection to the users database."""
    return sqlite3.connect(Config.DATABASE_PATH)


def init_user_database() -> None:
    """Create the users table when the application starts."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                verified INTEGER DEFAULT 0,
                mobile TEXT,
                role TEXT DEFAULT 'user'
            )
            """
        )
        connection.commit()
    logger.info("User database initialized at %s", Config.DATABASE_PATH)


def create_user(
    name: str,
    email: str,
    password: str,
    mobile: str = "",
) -> tuple[bool, str | None]:
    """Register a new user. Returns (success, error_message)."""
    password_hash = generate_password_hash(password)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (name, email, password, mobile)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, password_hash, mobile),
            )
            connection.commit()
        return True, None
    except sqlite3.IntegrityError:
        logger.info("Registration rejected: user already exists (%s)", email)
        return False, "User already exists"


def authenticate_user(identifier: str, password: str) -> dict | None:
    """Validate login credentials and return a session-safe user dict."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, name, email, password, verified, mobile, role
            FROM users
            WHERE email = ? OR mobile = ? OR name = ?
            """,
            (identifier, identifier, identifier),
        )
        user_row = cursor.fetchone()

    if not user_row or not check_password_hash(user_row[3], password):
        return None

    return {
        "id": user_row[0],
        "name": user_row[1],
        "email": user_row[2],
        "mobile": user_row[5],
        "role": user_row[6],
    }
