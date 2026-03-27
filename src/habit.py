"""Defines the core Habit Object-Oriented data model."""

from datetime import datetime
from typing import Optional


class Habit:
    """
    Represents a single habit in the tracking application.

    Attributes:
        name (str): The name of the habit (e.g., 'Drink Water').
        description (str): A short description of the habit.
        periodicity (str): The habit periodicity ('daily' or 'weekly').
        created_at (datetime): The timestamp when the habit was created.
        id (int, optional): The database primary key ID. Defaults to None until saved.
        checkoff_dates (list[datetime]): A list of timestamps when the habit was completed.
    """

    def __init__(
        self,
        name: str,
        description: str,
        periodicity: str,
        created_at: Optional[datetime] = None,
        habit_id: Optional[int] = None,
        checkoff_dates: Optional[list[datetime]] = None,
    ):
        self.id = habit_id
        self.name = name
        self.description = description
        self.periodicity = periodicity

        # If no creation date is provided (e.g., creating a new habit), use now()
        self.created_at = created_at if created_at else datetime.now()

        # If no check-off dates are provided, initialize an empty list
        self.checkoff_dates = checkoff_dates if checkoff_dates else []

    def mark_completed(self, completion_time: Optional[datetime] = None) -> bool:
        """
        Records a completion timestamp for the habit.

        Args:
            completion_time (datetime, optional): The time of completion. Defaults to now.

        Returns:
            bool: True indicating the habit was successfully marked.
        """
        if completion_time is None:
            completion_time = datetime.now()

        self.checkoff_dates.append(completion_time)
        return True

    def is_broken(self) -> bool:
        """
        Determines if the habit is currently broken.
        A daily habit is broken if more than 1 calendar day has passed since the last action.
        A weekly habit is broken if more than 7 calendar days have passed.

        Returns:
            bool: True if the habit is broken, False otherwise.
        """
        now = datetime.now().date()

        # Determine the baseline date (last completion, or creation if never completed)
        if self.checkoff_dates:
            # Get the most recent check-off date
            last_date = max(self.checkoff_dates).date()
        else:
            last_date = self.created_at.date()

        # Calculate the difference in calendar days between now and the most recent check-off date
        days_since_last = (now - last_date).days

        if self.periodicity == "daily":
            # For daily habits, if more than 1 day has passed (e.g., missed yesterday), it is broken
            return days_since_last > 1
        elif self.periodicity == "weekly":
            # For weekly habits, if more than 7 days have passed, it is broken
            return days_since_last > 7

        return False

    def __str__(self) -> str:
        """Returns a readable string representation of the Habit."""
        return f"[{self.periodicity.upper()}] {self.name} (ID: {self.id})"
