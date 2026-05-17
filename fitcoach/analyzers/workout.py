"""Workout parser and tracker."""

import json
import logging
import httpx

logger = logging.getLogger("fitcoach.workout")


class WorkoutAnalyzer:
    """Parse and track workouts using MiMo reasoning."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def parse(self, text: str) -> dict | None:
        """Parse a workout description into structured data."""
        prompt = f"""Parse this workout description into JSON:
"{text}"

Return:
{{
  "name": "workout name (e.g. Push Day, Leg Day, Run)",
  "type": "strength|cardio|flexibility|mixed",
  "duration_min": estimated_minutes,
  "exercises": [
    {{
      "name": "exercise name",
      "sets": number_or_null,
      "reps": number_or_null,
      "weight_kg": number_or_null,
      "distance_km": number_or_null,
      "duration_min": number_or_null
    }}
  ],
  "est_calories": estimated_kcal,
  "notes": "brief observation"
}}
Return ONLY the JSON."""

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.xiaomimimo.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 800,
                    },
                    timeout=15,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return json.loads(content.strip("` \n").replace("json\n", "", 1))
                return None

        except Exception as e:
            logger.error("Workout parse error: %s", e)
            return None

    def format_workout(self, workout: dict) -> str:
        """Format workout as readable message."""
        exercises = workout.get("exercises", [])

        lines = [
            f"🏋️ <b>Workout logged — {workout.get('name', 'Workout')}</b>",
            "",
            "📋 <b>Exercises:</b>",
        ]

        for ex in exercises:
            parts = [f"• {ex['name']}"]
            if ex.get("sets") and ex.get("reps"):
                parts.append(f": {ex['sets']}×{ex['reps']}")
            if ex.get("weight_kg"):
                parts.append(f" @ {ex['weight_kg']}kg")
            if ex.get("distance_km"):
                parts.append(f" {ex['distance_km']}km")
            if ex.get("duration_min"):
                parts.append(f" {ex['duration_min']}min")
            lines.append("".join(parts))

        if workout.get("est_calories"):
            lines.extend(["", f"🔥 Est. calories burned: ~{workout['est_calories']} kcal"])

        if workout.get("notes"):
            lines.extend(["", f"💡 {workout['notes']}"])

        return "\n".join(lines)

    async def answer_question(self, question: str, config) -> str:
        """Answer general fitness questions."""
        context = f"""You are FitCoach, an AI fitness assistant. 
User profile: {config.user.weight_kg}kg, {config.user.height_cm}cm, {config.user.age}y, goal: {config.user.goal}
Answer this fitness/nutrition question concisely and practically:
"{question}" """

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.xiaomimimo.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": context}],
                        "max_tokens": 500,
                    },
                    timeout=15,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                return "Couldn't process your question right now."

        except Exception as e:
            logger.error("Question error: %s", e)
            return "Error processing question."
