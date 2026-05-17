"""Configuration management for FitCoach."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class UserProfile:
    """User physical profile."""
    weight_kg: float = 70.0
    height_cm: float = 175.0
    age: int = 28
    gender: str = "male"
    goal: str = "muscle_gain"  # muscle_gain, fat_loss, maintain, endurance
    activity_level: str = "moderate"  # sedentary, light, moderate, active, very_active


@dataclass
class Config:
    """Main configuration."""
    # AI Engine
    mimo_api_key: str = ""
    mimo_model: str = "mimo-v2.5-pro"
    mimo_vision_model: str = "mimo-v2.5-pro"
    mimo_tts_model: str = "mimo-tts"

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # User Profile
    user: UserProfile = field(default_factory=UserProfile)

    # Database
    db_path: str = "data/fitcoach.db"

    # Coaching
    daily_briefing_hour: int = 8  # WIB
    calorie_target: int = 2200
    protein_target_g: int = 140
    carb_target_g: int = 250
    fat_target_g: int = 70


def load_config() -> Config:
    """Load configuration from environment."""
    return Config(
        mimo_api_key=os.getenv("MIMO_API_KEY", ""),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        user=UserProfile(
            weight_kg=float(os.getenv("USER_WEIGHT_KG", "70")),
            height_cm=float(os.getenv("USER_HEIGHT_CM", "175")),
            age=int(os.getenv("USER_AGE", "28")),
            gender=os.getenv("USER_GENDER", "male"),
            goal=os.getenv("USER_GOAL", "muscle_gain"),
            activity_level=os.getenv("USER_ACTIVITY_LEVEL", "moderate"),
        ),
        db_path=os.getenv("DB_PATH", "data/fitcoach.db"),
        calorie_target=int(os.getenv("CALORIE_TARGET", "2200")),
        protein_target_g=int(os.getenv("PROTEIN_TARGET_G", "140")),
        carb_target_g=int(os.getenv("CARB_TARGET_G", "250")),
        fat_target_g=int(os.getenv("FAT_TARGET_G", "70")),
    )
