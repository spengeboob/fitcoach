"""Progress tracking and pattern analysis."""

import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("fitcoach.progress")

WIB = timezone(timedelta(hours=7))


class ProgressTracker:
    """Track progress and detect patterns."""

    def __init__(self, config, food_analyzer, workout_analyzer):
        self.config = config
        self.food = food_analyzer
        self.workout = workout_analyzer

    def format_weekly(self, weekly: dict) -> str:
        """Format weekly summary."""
        lines = [
            "📊 <b>Weekly Summary</b>",
            "",
            f"🍽️ <b>Nutrition:</b>",
            f"   Avg calories: {weekly.get('avg_calories', 0):,.0f} kcal/day",
            f"   Avg protein: {weekly.get('avg_protein', 0):.0f}g/day",
            f"   Meals logged: {weekly.get('meal_count', 0)}",
            "",
            f"🏋️ <b>Workouts:</b>",
            f"   Sessions: {weekly.get('workout_count', 0)}",
            f"   Total volume: {weekly.get('total_volume_kg', 0):,.0f} kg",
            f"   Est. calories burned: {weekly.get('total_calories_burned', 0):,.0f} kcal",
        ]

        # Streak
        streak = weekly.get("logging_streak", 0)
        if streak > 0:
            lines.extend(["", f"🔥 Logging streak: {streak} days"])

        return "\n".join(lines)

    def generate_briefing(self, daily: dict, weekly: dict, config) -> str:
        """Generate a morning briefing text."""
        now = datetime.now(WIB)

        lines = [
            f"Good morning! Here's your {now.strftime('%A')} briefing.",
            "",
        ]

        # Yesterday's nutrition
        yday_cal = daily.get("calories", 0)
        yday_pro = daily.get("protein_g", 0)
        cal_target = config.calorie_target
        pro_target = config.protein_target_g

        if yday_cal > 0:
            pro_pct = int(yday_pro / pro_target * 100) if pro_target else 0
            lines.append(
                f"Yesterday you consumed {yday_cal:,} calories with {yday_pro:.0f}g protein "
                f"({pro_pct}% of target)."
            )
        else:
            lines.append("No meals logged yesterday. Try to log at least one meal today!")

        # Workout trend
        workout_count = weekly.get("workout_count", 0)
        if workout_count > 0:
            lines.append(f"You've worked out {workout_count} times this week. Great consistency!")
        else:
            lines.append("No workouts logged this week yet. Even a 20-minute walk counts!")

        # Suggestions
        lines.extend(["", "Today's tip: Focus on hydration — aim for at least 2.5 liters of water."])

        return "\n".join(lines)
