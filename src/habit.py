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
        checkoff_dates: Optional[list[datetime]] = None
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

    def __str__(self) -> str:
        """Returns a readable string representation of the Habit."""
        return f"[{self.periodicity.upper()}] {self.name} (ID: {self.id})"