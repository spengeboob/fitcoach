"""Database layer for FitCoach."""

import sqlite3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("fitcoach.db")

WIB = timezone(timedelta(hours=7))


class Database:
    """SQLite database for meals, workouts, and progress."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                dishes TEXT NOT NULL,
                calories REAL DEFAULT 0,
                protein_g REAL DEFAULT 0,
                carbs_g REAL DEFAULT 0,
                fat_g REAL DEFAULT 0,
                fiber_g REAL DEFAULT 0,
                notes TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                duration_min INTEGER,
                exercises TEXT NOT NULL,
                est_calories INTEGER DEFAULT 0,
                notes TEXT
            )
        """)

        conn.commit()
        conn.close()

    def log_meal(self, analysis: dict):
        """Log a meal from food analysis."""
        import json
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        total = analysis.get("total", {})
        c.execute(
            "INSERT INTO meals (timestamp, dishes, calories, protein_g, carbs_g, fat_g, fiber_g, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                datetime.now(WIB).isoformat(),
                json.dumps(analysis.get("dishes", [])),
                total.get("calories", 0),
                total.get("protein_g", 0),
                total.get("carbs_g", 0),
                total.get("fat_g", 0),
                total.get("fiber_g", 0),
                analysis.get("notes", ""),
            ),
        )
        conn.commit()
        conn.close()

    def log_workout(self, workout: dict):
        """Log a workout."""
        import json
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute(
            "INSERT INTO workouts (timestamp, name, type, duration_min, exercises, est_calories, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                datetime.now(WIB).isoformat(),
                workout.get("name", "Workout"),
                workout.get("type", "mixed"),
                workout.get("duration_min", 0),
                json.dumps(workout.get("exercises", [])),
                workout.get("est_calories", 0),
                workout.get("notes", ""),
            ),
        )
        conn.commit()
        conn.close()

    def get_today_totals(self) -> dict:
        """Get today's nutrition totals."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        today = datetime.now(WIB).date().isoformat()
        c.execute(
            "SELECT SUM(calories), SUM(protein_g), SUM(carbs_g), SUM(fat_g) FROM meals WHERE timestamp LIKE ?",
            (f"{today}%",),
        )
        row = c.fetchone()
        conn.close()

        return {
            "calories": row[0] or 0,
            "protein_g": row[1] or 0,
            "carbs_g": row[2] or 0,
            "fat_g": row[3] or 0,
        }

    def get_weekly_summary(self) -> dict:
        """Get this week's summary."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        week_ago = (datetime.now(WIB) - timedelta(days=7)).isoformat()

        # Nutrition
        c.execute(
            "SELECT AVG(calories), AVG(protein_g), COUNT(*) FROM meals WHERE timestamp >= ?",
            (week_ago,),
        )
        meal_row = c.fetchone()

        # Workouts
        c.execute(
            "SELECT COUNT(*), SUM(est_calories) FROM workouts WHERE timestamp >= ?",
            (week_ago,),
        )
        workout_row = c.fetchone()

        # Logging streak
        c.execute(
            "SELECT DISTINCT date(timestamp) FROM meals ORDER BY date(timestamp) DESC"
        )
        dates = [r[0] for r in c.fetchall()]
        streak = 0
        today = datetime.now(WIB).date()
        for i, d in enumerate(dates):
            expected = (today - timedelta(days=i)).isoformat()
            if d == expected:
                streak += 1
            else:
                break

        conn.close()

        return {
            "avg_calories": meal_row[0] or 0,
            "avg_protein": meal_row[1] or 0,
            "meal_count": meal_row[2] or 0,
            "workout_count": workout_row[0] or 0,
            "total_calories_burned": workout_row[1] or 0,
            "total_volume_kg": 0,  # TODO: calculate from exercises
            "logging_streak": streak,
        }
