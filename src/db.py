"""Manages SQLite database connections and CRUD operations."""

import sqlite3
from datetime import datetime
from src.habit import Habit


class DatabaseManager:
    """
    Manages all database operations for the Habit Tracker using SQLite.
    Strictly encapsulates the database connection to prevent outside interference.
    """

    def __init__(self, db_name: str = "data/habits.db"):
        # The single underscore is used to indicate these are 'private' to this class
        self._db_name = db_name
        self._conn = None
        self.connect()
        self.create_tables()

    def connect(self) -> None:
        """Establishes a connection to the SQLite database."""
        self._conn = sqlite3.connect(self._db_name)
        # Enable foreign keys for cascading deletes (deletes all habit check-off logs when the habit is deleted)
        self._conn.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self) -> None:
        """Creates the necessary tables if they don't already exist."""
        cursor = self._conn.cursor()

        # Table for storing habit metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Table for storing the check-off timestamps (1-to-Many relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        """)

        self._conn.commit()

    def insert_habit(self, habit: Habit) -> bool:
        """Saves a new Habit object to the database and assigns it an ID."""
        cursor = self._conn.cursor()

        # ISO format to cleanly store dates as strings in SQLite
        cursor.execute(
            """
            INSERT INTO habits (name, description, periodicity, created_at)
            VALUES (?, ?, ?, ?)
        """,
            (
                habit.name,
                habit.description,
                habit.periodicity,
                habit.created_at.isoformat(),
            ),
        )

        self._conn.commit()

        # Update the Python object with its new database ID
        habit.id = cursor.lastrowid
        return True

    def delete_habit(self, habit_id: int) -> bool:
        """Deletes a habit and its associated check-offs from the database."""
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self._conn.commit()
        return True

    def log_completion(self, habit_id: int, timestamp: datetime) -> None:
        """Saves a check-off timestamp for a specific habit."""
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO checkoffs (habit_id, timestamp)
            VALUES (?, ?)
        """,
            (habit_id, timestamp.isoformat()),
        )
        self._conn.commit()

    def get_all_habits(self) -> list[Habit]:
        """Retrieves all habits and their check-off history from the database."""
        cursor = self._conn.cursor()

        # 1. Fetch all habits
        cursor.execute(
            "SELECT id, name, description, periodicity, created_at FROM habits"
        )
        habit_rows = cursor.fetchall()

        habits = []
        for row in habit_rows:
            habit_id, name, description, periodicity, created_at_str = row

            # Convert the string back into a Python datetime object
            created_at = datetime.fromisoformat(created_at_str)

            # 2. Fetch all check-offs for this specific habit
            cursor.execute(
                "SELECT timestamp FROM checkoffs WHERE habit_id = ?", (habit_id,)
            )
            checkoff_rows = cursor.fetchall()

            # Use list comprehension to quickly parse all timestamps
            checkoff_dates = [
                datetime.fromisoformat(c_row[0]) for c_row in checkoff_rows
            ]

            # 3. Reconstruct the Habit object
            habit = Habit(
                name=name,
                description=description,
                periodicity=periodicity,
                created_at=created_at,
                habit_id=habit_id,
                checkoff_dates=checkoff_dates,
            )
            habits.append(habit)

        return habits
