"""Automated script to generate 5 predefined habits and 4 weeks of test data."""

import os
from datetime import datetime, timedelta
from src.db import DatabaseManager
from src.habit import Habit


def generate_predefined_data():
    """
    Clears the existing database and populates it with 5 predefined habits
    and 4 weeks of historical check-off data.
    """
    db_path = "data/habits.db"

    # Start fresh by deleting the old database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Old database removed.")

    # Initialize a fresh database
    db = DatabaseManager(db_name=db_path)
    print("Fresh database created.")

    # Define the 5 habits (Mixture of daily and weekly)
    predefined_habits = [
        Habit(
            name="Drink Water",
            description="Drink 2 liters of water",
            periodicity="daily",
        ),
        Habit(name="Read a Book", description="Read 20 pages", periodicity="daily"),
        Habit(name="Exercise", description="30 mins of cardio", periodicity="daily"),
        Habit(name="Clean House", description="Vacuum and dust", periodicity="weekly"),
        Habit(
            name="Study Python",
            description="Work on Python projects",
            periodicity="weekly",
        ),
    ]

    # Insert habits into the database to get their IDs
    for habit in predefined_habits:
        db.insert_habit(habit)

    # Generate 4 weeks (28 days) of historical data
    print("Generating 4 weeks of historical tracking data...")
    today = datetime.now()
    start_date = today - timedelta(days=27)

    # Simulate a perfect 28-day streak for the first habit,
    # and realistic "missed days" for the others.

    for i in range(28):
        current_date = start_date + timedelta(days=i)

        # Habit 1: Drink Water (Perfect daily streak - 28 days)
        db.log_completion(predefined_habits[0].id, current_date)

        # Habit 2: Read a Book (Missed a few days, so streak is broken)
        if i % 3 != 0:  # Skips every 3rd day
            db.log_completion(predefined_habits[1].id, current_date)

        # Habit 3: Exercise (Daily, but only did it the first 2 weeks)
        if i < 14:
            db.log_completion(predefined_habits[2].id, current_date)

        # Habit 4: Clean House (Weekly - perfect 4 week streak)
        # Check off once every 7 days
        if i % 7 == 0:
            db.log_completion(predefined_habits[3].id, current_date)

        # Habit 5: Study Python (Weekly - missed the 3rd week)
        if i % 7 == 0 and i != 21:
            db.log_completion(predefined_habits[4].id, current_date)

    print("Fixtures successfully loaded! 5 Habits and 4 weeks of data added.")
    print("You can now run 'python src/main.py' to view the analytics.")


if __name__ == "__main__":
    generate_predefined_data()
