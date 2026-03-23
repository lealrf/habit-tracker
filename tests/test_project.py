import pytest
from datetime import datetime, timedelta
from src.habit import Habit
from src.db import DatabaseManager
import src.analytics as analytics

@pytest.fixture
def temp_db():
    """
    Creates a temporary, in-memory SQLite database for isolated testing.
    It automatically gets destroyed after the tests finish.
    """
    # ':memory:' is a special SQLite command for a RAM-only database
    db = DatabaseManager(":memory:")
    yield db
    # Teardown: close the connection after the test
    db._conn.close()

def test_habit_creation():
    """Tests if a Habit object is correctly initialized."""
    habit = Habit(name="Test Habit", description="Testing", periodicity="daily")
    
    assert habit.name == "Test Habit"
    assert habit.periodicity == "daily"
    assert habit.checkoff_dates ==[]
    # ID should be None before inserting into the database
    assert habit.id is None 

def test_database_insert_and_retrieve(temp_db):
    """Tests if the DatabaseManager can save and load habits."""
    habit = Habit(name="Run", description="5km", periodicity="daily")
    
    # Insert should assign an ID
    temp_db.insert_habit(habit)
    assert habit.id is not None
    
    # Retrieve from DB and check if it matches
    loaded_habits = temp_db.get_all_habits()
    assert len(loaded_habits) == 1
    assert loaded_habits[0].name == "Run"

def test_habit_completion_and_is_broken(temp_db):
    """Tests checking off a habit and the is_broken logic."""
    habit = Habit(name="Read", description="10 pages", periodicity="daily")
    temp_db.insert_habit(habit)
    
    # Log a completion for today
    today = datetime.now()
    habit.mark_completed(today)
    temp_db.log_completion(habit.id, today)
    
    # Habit was completed today, so it shouldn't be broken
    assert habit.is_broken() is False
    
    # Simulate a habit completed 3 days ago
    old_habit = Habit(name="Old", description="", periodicity="daily")
    three_days_ago = today - timedelta(days=3)
    old_habit.mark_completed(three_days_ago)
    
    # Because it's a daily habit and 3 days have passed, it SHOULD be broken
    assert old_habit.is_broken() is True

def test_analytics_longest_streak():
    """Tests the functional analytics streak calculator."""
    habit = Habit("Test", "Test", "daily")
    today = datetime.now()
    
    # Simulate checking it off for 3 consecutive days
    habit.mark_completed(today - timedelta(days=2))
    habit.mark_completed(today - timedelta(days=1))
    habit.mark_completed(today)
    
    # The streak should be exactly 3
    streak = analytics.calculate_longest_streak(habit)
    assert streak == 3

def test_analytics_broken_streak():
    """Tests if the streak correctly resets when a day is missed."""
    habit = Habit("Test", "Test", "daily")
    today = datetime.now()
    
    # Checked off 4 days ago, 3 days ago, MISSED 2 days ago, checked off yesterday and today.
    # The longest streak was 2 (either the first block or the second block)
    habit.mark_completed(today - timedelta(days=4))
    habit.mark_completed(today - timedelta(days=3))
    # -- Missed day --
    habit.mark_completed(today - timedelta(days=1))
    habit.mark_completed(today)
    
    streak = analytics.calculate_longest_streak(habit)
    assert streak == 2