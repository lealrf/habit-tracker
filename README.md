# 🚀 Professional Habit Tracker

A robust, backend-focused Habit Tracking Application built with Python. This project was developed to demonstrate a strict separation of concerns by combining **Object-Oriented Programming (OOP)** for data management and **Functional Programming (FP)** for stateless data analytics.

**Environment:** Built and natively tested on **macOS (Apple Silicon)** using **Python 3.12**. Fully compatible with Windows and Linux.

---

## ✨ Core Features
*   **Interactive CLI:** A beautiful, crash-proof terminal interface using arrow-key navigation (`questionary`).
*   **Persistent Storage:** Custom OOP `DatabaseManager` utilizing **SQLite** for ACID-compliant, relational data storage.
*   **Functional Analytics:** A dedicated analytics engine built entirely with pure functions, heavily utilizing `map()`, `filter()`, and `reduce()` to calculate streaks and filter data.
*   **Smart Streak Tracking:** Chronological date math prevents artificial streak inflation (e.g., checking off a habit twice in one day).

---

## ⚙️ Prerequisites
*   **Python 3.7+** (Python 3.12 is highly recommended)
*   Git (to clone the repository)

---

## 💻 Installation & Setup

First, clone the repository to your local machine and navigate into the project directory:

```bash
git clone https://github.com/lealrf/habit-tracker.git
cd habit-tracker
```

To ensure dependency isolation, please install the application inside a Virtual Environment (`venv`). 

### 🍎 For macOS / Linux:
Open your terminal and run the following commands from the root directory of the project:

```bash
# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install the required dependencies
python3 -m pip install -r requirements.txt
```

### 🪟 For Windows:
Open Command Prompt or PowerShell and run::

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate the virtual environment
venv\Scripts\activate

# 3. Install the required dependencies
pip install -r requirements.txt
```

---

## 🧪 Loading Test Data (Fixtures)
To easily evaluate the application, a fixture script is included. This script automatically deletes any existing database and generates a fresh SQLite database containing 5 predefined habits (Daily & Weekly) and exactly 4 weeks (28 days) of realistic historical check-off data.
Run this command to load the test data:
```bash
python -m src.setup_fixtures
```

---

## 🚀 How to Run the Application
Once the dependencies are installed and the virtual environment is active, launch the main interactive CLI by running:
```bash
python -m src.main
```

Example Usage:
* **1.** Use your **Arrow** Keys to navigate the menu.
* **2.** Select "**3. View Analytics**" to see the purely functional dashboard calculate your longest streaks across the predefined 4-week test data.
* **3.** Select "**2. Check-off a habit**" to log a new completion timestamp instantly.

---


### 🛡️ Running the Test Suite
The application is secured by a comprehensive pytest suite that verifies the OOP models, database insertion logic, and functional analytics. To ensure maximum data safety, the tests use @pytest.fixture to run entirely inside an isolated, in-memory SQLite database (:memory:), meaning your real habit data will never be touched.
To run the tests and see detailed output for each individual test, run:

```bash
pytest -v tests/
```

---


### 📂 Project Structure
```text
habit_tracker/
├── src/
│   ├── analytics.py      # Pure functional programming module
│   ├── db.py             # OOP SQLite Database Manager
│   ├── habit.py          # OOP Habit Data Model
│   ├── main.py           # Presentation Layer (CLI Router)
│   └── setup_fixtures.py # Automated test-data generator
├── tests/
│   └── test_project.py   # Comprehensive pytest suite
├── data/
│   └── habits.db         # Auto-generated SQLite database
├── README.md             # Project documentation
└── requirements.txt      # Dependency list
```