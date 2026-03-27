"""Purely functional module for calculating habit streaks and statistics."""

from functools import reduce
from src.habit import Habit


def list_all_habits(habits: list[Habit]) -> list[str]:
    """
    Returns a list of formatted strings representing all habits.
    Uses map() to transform Habit objects into readable strings.
    """
    return list(map(lambda h: str(h), habits))


def filter_by_periodicity(habits: list[Habit], periodicity: str) -> list[Habit]:
    """
    Filters the list of habits by their periodicity ('daily' or 'weekly').
    Uses filter() to keep only the habits matching the periodicity criteria.
    """
    return list(filter(lambda h: h.periodicity.lower() == periodicity.lower(), habits))


def calculate_longest_streak(habit: Habit) -> int:
    """
    Calculates the longest streak for a single habit.
    A purely functional approach analyzing the sorted checkoff_dates.
    """
    if not habit.checkoff_dates:
        return 0

    # Sort the dates to ensure chronological order
    sorted_dates = sorted([d.date() for d in habit.checkoff_dates])

    # Remove duplicates in case a user checked off a habit twice in one day
    unique_dates = sorted(list(set(sorted_dates)))

    if not unique_dates:
        return 0

    max_streak = 1
    current_streak = 1

    for i in range(1, len(unique_dates)):
        # Calculate days between the current date and the previous date
        days_diff = (unique_dates[i] - unique_dates[i - 1]).days

        # If the gap matches the periodicity, the streak continues
        if (habit.periodicity == "daily" and days_diff == 1) or (
            habit.periodicity == "weekly" and days_diff <= 7
        ):
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            # Streak broken, reset to 1
            current_streak = 1

    return max_streak


def calculate_longest_streak_overall(habits: list[Habit]) -> int:
    """
    Calculates the absolute longest streak across all provided habits.
    Uses map() to get all streaks, and reduce() to find the maximum.
    """
    if not habits:
        return 0

    # Transform the list of Habit objects into a list of integer streaks using map()
    streaks = list(map(calculate_longest_streak, habits))

    # Continually compare two items and keep the larger one to find the max using reduce()
    longest = reduce(lambda a, b: a if a > b else b, streaks)

    return longest
