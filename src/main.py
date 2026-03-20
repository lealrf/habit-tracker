import os
import sys
from datetime import datetime
import questionary
from src.db import DatabaseManager
from src.habit import Habit
import src.analytics as analytics

def clear_screen():
    """Clears the terminal screen for a clean UI. Works on Mac/Linux and Windows."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Prints the application header."""
    print("\n" + "="*50)
    print(" 📋 HABIT TRACKER")
    print("="*50 + "\n")

def add_habit(db: DatabaseManager):
    """Prompts the user to create a new habit and saves it to the database."""
    name = questionary.text("What is the name of your new habit?").ask()
    desc = questionary.text("Enter a short description:").ask()
    periodicity = questionary.select(
        "How often do you want to complete this habit?",
        choices=["daily", "weekly"]
    ).ask()

    new_habit = Habit(name=name, description=desc, periodicity=periodicity)
    db.insert_habit(new_habit)
    print(f"\n✅ Success! Habit '{name}' successfully created.")

def checkoff_habit(db: DatabaseManager):
    """Allows the user to select a habit and mark it as completed right now."""
    habits = db.get_all_habits()
    if not habits:
        print("\n❌ You don't have any habits yet. Please add one first.")
        return

    # Create a list of choices for the interactive menu
    choices =[questionary.Choice(title=h.name, value=h) for h in habits]
    
    selected_habit = questionary.select(
        "Which habit would you like to check off?",
        choices=choices
    ).ask()

    # Mark the habit as completed in the Python object and save it to the SQLite DB
    now = datetime.now()
    selected_habit.mark_completed(now)
    db.log_completion(selected_habit.id, now)
    
    print(f"\n🎉 Great job! You checked off '{selected_habit.name}'.")

def delete_habit(db: DatabaseManager):
    """Allows the user to select and delete a habit."""
    habits = db.get_all_habits()
    if not habits:
        print("\n❌ No habits to delete.")
        return

    choices = [questionary.Choice(title=h.name, value=h) for h in habits]
    selected_habit = questionary.select(
        "Which habit do you want to delete?",
        choices=choices
    ).ask()

    # Confirm deletion
    confirm = questionary.confirm(f"Are you sure you want to delete '{selected_habit.name}'?").ask()
    if confirm:
        db.delete_habit(selected_habit.id)
        print(f"\n🗑️ Habit '{selected_habit.name}' deleted.")

def view_analytics(db: DatabaseManager):
    """Displays the analytics dashboard using pure functional programming."""
    habits = db.get_all_habits()
    if not habits:
        print("\n❌ You don't have any habits yet. Not enough data for analytics.")
        return

    print("\n" + "-"*40)
    print(" 📊 ANALYTICS DASHBOARD")
    print("-"*40)

    # 1. List all habits using the functional map()
    print("\n=> ALL CURRENT HABITS:")
    for h_str in analytics.list_all_habits(habits):
        print(f"   {h_str}")

    # 2. Filter by periodicity using functional filter()
    daily_habits = analytics.filter_by_periodicity(habits, "daily")
    print(f"\n=> YOU HAVE {len(daily_habits)} DAILY HABITS.")

    # 3. Overall longest streak using map() and reduce()
    longest_overall = analytics.calculate_longest_streak_overall(habits)
    print(f"\n🔥 LONGEST STREAK OVERALL: {longest_overall} completions in a row!")

    # 4. Longest streak for a specific habit
    print("\n=> CHECK STREAK FOR A SPECIFIC HABIT:")
    choices =[questionary.Choice(title=h.name, value=h) for h in habits]
    selected_habit = questionary.select(
        "Select a habit to analyze:",
        choices=choices
    ).ask()
    
    streak = analytics.calculate_longest_streak(selected_habit)
    print(f"   The longest streak for '{selected_habit.name}' is {streak}.")
    print("-" * 40 + "\n")

def main():
    """Main application loop."""
    # Initialize our Encapsulated OOP Database
    db = DatabaseManager()
    
    while True:
        clear_screen()
        display_header()
        
        # Interactive Arrow-Key Menu
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "1. Add a new habit",
                "2. Check-off a habit",
                "3. View Analytics",
                "4. Delete a habit",
                "5. Exit"
            ]
        ).ask()

        # Route the user's choice to the correct function
        if action == "1. Add a new habit":
            add_habit(db)
            input("\nPress Enter to return to the menu...")
        elif action == "2. Check-off a habit":
            checkoff_habit(db)
            input("\nPress Enter to return to the menu...")
        elif action == "3. View Analytics":
            view_analytics(db)
            input("\nPress Enter to return to the menu...")
        elif action == "4. Delete a habit":
            delete_habit(db)
            input("\nPress Enter to return to the menu...")
        elif action == "5. Exit":
            clear_screen()
            print("\n👋 Keep up the good habits! See you later.\n")
            sys.exit(0)

if __name__ == "__main__":
    main()