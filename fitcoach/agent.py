"""Main FitCoach agent — processes food photos and workout logs."""

import asyncio
import logging
from datetime import datetime, timezone, timedelta

from fitcoach.config import Config
from fitcoach.analyzers.food import FoodAnalyzer
from fitcoach.analyzers.workout import WorkoutAnalyzer
from fitcoach.analyzers.progress import ProgressTracker
from fitcoach.delivery.telegram import TelegramDelivery
from fitcoach.delivery.voice import VoiceDelivery
from fitcoach.utils.database import Database

logger = logging.getLogger("fitcoach.agent")

WIB = timezone(timedelta(hours=7))


class FitCoachAgent:
    """AI fitness & nutrition analyst with voice coaching."""

    def __init__(self, config: Config):
        self.config = config
        self.food = FoodAnalyzer(config.mimo_api_key, config.mimo_vision_model)
        self.workout = WorkoutAnalyzer(config.mimo_api_key, config.mimo_model)
        self.progress = ProgressTracker(config, self.food, self.workout)
        self.telegram = TelegramDelivery(config.telegram_bot_token, config.telegram_chat_id)
        self.voice = VoiceDelivery(config.mimo_api_key)
        self.db = Database(config.db_path)
        self.last_briefing_date = None

    async def run(self):
        """Main agent loop — listens for Telegram messages."""
        logger.info("FitCoach agent started at %s", datetime.now(WIB).strftime("%H:%M WIB"))

        offset = 0
        while True:
            try:
                messages = await self.telegram.get_updates(offset)
                for msg in messages:
                    offset = msg["update_id"] + 1
                    await self._handle_message(msg)
            except Exception as e:
                logger.error("Agent tick failed: %s", e, exc_info=True)

            # Check for daily briefing
            await self._check_daily_briefing()

            await asyncio.sleep(2)

    async def _handle_message(self, update: dict):
        """Handle incoming Telegram message."""
        message = update.get("message", {})
        chat_id = str(message.get("chat", {}).get("id", ""))

        if chat_id != self.config.telegram_chat_id:
            return

        # Photo → food analysis
        if "photo" in message:
            await self._handle_food_photo(message)
            return

        # Text → workout log or query
        text = message.get("text", "").strip()
        if not text:
            return

        text_lower = text.lower()
        if any(kw in text_lower for kw in ["ran", "walked", "push", "pull", "leg", "bench", "squat", "deadlift", "curl", "press", "km", "kg", "reps", "sets", "cardio", "swim", "bike"]):
            await self._handle_workout_log(text)
        elif any(kw in text_lower for kw in ["progress", "summary", "how am i", "stats", "weight"]):
            await self._handle_progress_query()
        elif any(kw in text_lower for kw in ["what should i eat", "suggest", "dinner", "lunch", "breakfast"]):
            await self._handle_meal_suggestion()
        else:
            await self._handle_general_query(text)

    async def _handle_food_photo(self, message: dict):
        """Analyze a food photo."""
        photos = message.get("photo", [])
        if not photos:
            return

        # Get highest resolution photo
        file_id = photos[-1]["file_id"]
        photo_path = await self.telegram.download_file(file_id)

        if not photo_path:
            await self.telegram.send("Couldn't download the photo. Try again?")
            return

        # Analyze with MiMo Vision
        analysis = await self.food.analyze_photo(photo_path)

        if analysis:
            # Save to database
            self.db.log_meal(analysis)

            # Format and send response
            response = self.food.format_analysis(analysis)
            await self.telegram.send(response)

            # Daily progress check
            daily = self.db.get_today_totals()
            progress_msg = self.food.format_daily_progress(daily, self.config)
            await self.telegram.send(progress_msg)
        else:
            await self.telegram.send("Couldn't analyze the food photo. Make sure it's clear and well-lit.")

    async def _handle_workout_log(self, text: str):
        """Parse and log a workout."""
        workout = await self.workout.parse(text)

        if workout:
            self.db.log_workout(workout)
            response = self.workout.format_workout(workout)
            await self.telegram.send(response)
        else:
            await self.telegram.send("Couldn't parse your workout. Try: 'bench press 4x8 at 60kg'")

    async def _handle_progress_query(self):
        """Show progress summary."""
        weekly = self.db.get_weekly_summary()
        response = self.progress.format_weekly(weekly)
        await self.telegram.send(response)

    async def _handle_meal_suggestion(self):
        """Suggest a meal based on remaining macros."""
        daily = self.db.get_today_totals()
        suggestion = await self.food.suggest_meal(daily, self.config)
        await self.telegram.send(suggestion)

    async def _handle_general_query(self, text: str):
        """Handle general fitness questions."""
        response = await self.workout.answer_question(text, self.config)
        await self.telegram.send(response)

    async def _check_daily_briefing(self):
        """Send daily voice briefing at configured hour."""
        now = datetime.now(WIB)
        if now.hour == self.config.daily_briefing_hour and self.last_briefing_date != now.date():
            self.last_briefing_date = now.date()

            # Generate briefing
            weekly = self.db.get_weekly_summary()
            daily = self.db.get_today_totals()
            briefing_text = self.progress.generate_briefing(daily, weekly, self.config)

            # Send text version
            await self.telegram.send(f"🌅 <b>Morning Briefing</b>\n\n{briefing_text}")

            # Send voice version
            voice_path = await self.voice.generate(briefing_text)
            if voice_path:
                await self.telegram.send_voice(voice_path)

            logger.info("Daily briefing delivered")
