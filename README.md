# 🏋️ FitCoach

**AI Fitness & Nutrition Analyst with Voice Coaching**

Snap your food, log your workout, get coached by AI. FitCoach uses Xiaomi MiMo's multimodal vision to analyze meals from photos, reasoning engine to track progress patterns, and TTS to deliver daily voice briefings — like having a personal trainer in your pocket.

![Architecture](https://img.shields.io/badge/Architecture-Agent--first-blue)
![Features](https://img.shields.io/badge/Features-Voice_%2B_Vision-green)
![Model](https://img.shields.io/badge/Powered_by-MiMo_V2.5-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What It Does

1. **📸 Snap** — photograph your meal
2. **🏋️ Log** — describe your workout in plain text
3. **🔊 Listen** — receive a voice briefing with insights, suggestions, and encouragement

No calorie counting. No barcode scanning. Just photos, text, and voice.

## How It Works

- Food photo → MiMo Vision identifies dishes, estimates portions, calculates macros
- Workout text → MiMo parses exercises, sets, reps, weight, estimates calories burned
- Daily digest → MiMo TTS generates personalized voice coaching with progress highlights and actionable tips
- All data stored in SQLite — meals, workouts, goals, trends

## Features

### 📸 Food Photo Analysis
- Snap a photo → MiMo Vision identifies dishes, estimates portions, calculates macros
- Tracks calories, protein, carbs, fat, fiber
- Recognizes cuisines from around the world
- Flags nutritional imbalances

### 🏋️ Workout Logging
- Describe workouts in plain text: "ran 5km in 25 min" or "push day, 4x10 bench press"
- MiMo parses exercise type, duration, sets, reps, weight
- Estimates calories burned
- Tracks progressive overload

### 🔊 Voice Coaching
- Daily audio briefing: nutrition summary, workout suggestions, progress update
- Personalized tips based on your patterns
- Motivational nudges when you're off-track
- Listen on the go — no app needed

### 📊 Progress Tracking
- Weekly/monthly trends for weight, body measurements, macros
- Pattern detection: "You tend to skip protein on weekdays"
- Goal setting and adjustment
- Visual progress charts (Telegram delivery)

### 💬 Conversational Interface
- Chat naturally via Telegram
- Ask questions: "How was my protein this week?"
- Get suggestions: "What should I eat for dinner?"
- Voice replies for hands-free interaction

## Usage Examples

**Food Analysis**

```
📸 [photo of nasi goreng with egg and chicken]

🍽️ Nasi Goreng with Egg & Chicken
   • Calories: ~520 kcal
   • Protein: 28g | Carbs: 62g | Fat: 18g

📊 Daily Progress: 1,240 / 2,200 kcal (56%)
   Protein: 68g / 140g (49%)

💡 You're low on protein today — consider Greek
   yogurt or a protein shake as a snack.
```

**Workout Logging**

```
🏋️ did chest and triceps. bench 4x8 @60kg, incline db
   3x10 @20kg, cable fly 3x12, tricep pushdown 3x15

📋 Logged — Push Day
   Bench Press 4×8 @60kg (240kg volume)
   Incline DB Press 3×10 @20kg
   Cable Fly 3×12 | Tricep Pushdown 3×15

🔥 ~280 kcal burned

📈 Bench volume +8% from last week — on track
```

**Voice Briefing**

```
🔊 [0:42 voice message]

"Good morning! Yesterday you hit 128g protein — 91% of
your target, solid effort. Workout volume trending up
for 3 weeks straight. Today's a rest day, so focus on
hydration and sleep. Tomorrow is legs — eat carbs tonight."
```

## Quick Start

```bash
git clone https://github.com/spengeboob/fitcoach.git
cd fitcoach
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
python -m fitcoach
```

## Configuration

```env
# AI Engine (Xiaomi MiMo)
MIMO_API_KEY=your_mimo_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# User Profile (optional, for personalized coaching)
USER_WEIGHT_KG=70
USER_HEIGHT_CM=175
USER_AGE=28
USER_GOAL=muscle_gain
USER_ACTIVITY_LEVEL=moderate
```

## Project Structure

```
fitcoach/
├── __init__.py
├── __main__.py          # Entry point
├── config.py            # Configuration
├── agent.py             # Main agent loop
├── analyzers/
│   ├── __init__.py
│   ├── food.py          # MiMo Vision food analysis
│   ├── workout.py       # Workout parsing & tracking
│   └── progress.py      # Progress analysis & patterns
├── delivery/
│   ├── __init__.py
│   ├── telegram.py      # Telegram bot (text + photo + voice)
│   └── voice.py         # MiMo TTS voice generation
├── utils/
│   ├── __init__.py
│   ├── database.py      # SQLite data layer
│   ├── nutrition.py     # Nutrition database (USDA)
│   └── formatting.py    # Output formatting
├── data/
│   └── nutrition.db     # Nutrition reference data
├── requirements.txt
├── .env.example
└── README.md
```

## Why MiMo?

| Capability | FitCoach Use Case |
|------------|-------------------|
| **Vision** (Multimodal) | Food photo → dish identification, portion estimation, macro calculation |
| **Reasoning** (MiMo-V2.5-Pro) | Pattern detection, progress analysis, personalized suggestions |
| **TTS** | Daily voice coaching briefings, hands-free feedback |

The combination of vision + reasoning + voice is unique to MiMo. Other models require separate services for each capability, adding latency and complexity.

## Roadmap

- [ ] Body photo progress tracking (visual diff over time)
- [ ] Barcode scanning for packaged foods
- [ ] Integration with wearable devices (Apple Watch, Fitbit)
- [ ] Meal planning with grocery lists
- [ ] Social features — share progress with friends
- [ ] Workout plan generation based on goals

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built by an independent developer · Powered by <a href="https://mimo.xiaomi.com/">Xiaomi MiMo</a>
</p>
