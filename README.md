# 🏋️ FitCoach

*Your AI gym buddy that sees what you eat, understands how you train, and talks to you about it.*

---

## Why I Built This

I kept failing at tracking my nutrition. Every fitness app I tried felt like a spreadsheet with a camera — snap a photo, manually adjust portion sizes, guess at ingredients, repeat. I'd quit within 10 days. Every. Single. Time.

So I asked: what if tracking felt like texting a friend who happens to know everything about nutrition?

That's FitCoach. You send a photo of your food, it tells you what's in it. You describe your workout in one sentence, it logs everything. And once a day, it sends you a voice message with coaching — like a personal trainer checking in, except it costs nothing and never judges your 2am snacks.

## How It Works

**Step 1: Snap your meal** → Send a food photo via Telegram. MiMo Vision identifies the dish, estimates portions, and breaks down macros (calories, protein, carbs, fat, fiber).

**Step 2: Log your workout** → Type something like "push day, bench 4x8 @60kg, cable fly 3x12". MiMo parses exercises, tracks volume, and estimates calories burned.

**Step 3: Listen to your coach** → Every morning, get a voice briefing covering yesterday's nutrition, workout progress, and what to focus on today.

No calorie databases. No barcode scanning. No manual data entry. Just photos, text, and voice.

## What's Under the Hood

Everything runs through a single MiMo-V2.5-Pro instance that handles:

- **Vision** — food photo analysis: dish identification, portion estimation, macro calculation
- **Reasoning** — pattern detection across meals and workouts, personalized suggestions, goal tracking
- **TTS** — natural voice coaching briefings delivered as Telegram voice messages

The data layer is SQLite — simple, portable, zero-config. Meals, workouts, goals, and trends are all persisted locally.

## Demo Conversations

**Food photo → instant breakdown:**

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

**Natural language workout logging:**

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

**Voice coaching (daily briefing):**

```
🔊 [0:42 voice message]

"Good morning! Yesterday you hit 128g protein — 91% of
your target, solid effort. Workout volume trending up
for 3 weeks straight. Today's a rest day, so focus on
hydration and sleep. Tomorrow is legs — eat carbs tonight."
```

## Getting Started

```bash
git clone https://github.com/spengeboob/fitcoach.git
cd fitcoach
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
python -m fitcoach
```

You'll need:
- A Telegram bot token ([@BotFather](https://t.me/BotFather))
- Xiaomi MiMo API key ([mimo.xiaomi.com](https://mimo.xiaomi.com/))
- (Optional) Your height, weight, and fitness goals for personalized coaching

## Project Map

```
fitcoach/
├── agent.py              # main loop — routes input, calls MiMo, delivers output
├── config.py             # env vars + user profile
├── analyzers/
│   ├── food.py           # MiMo Vision → dish ID + macro estimation
│   ├── workout.py        # parse free-text workout descriptions
│   └── progress.py       # trend detection + pattern recognition
├── delivery/
│   ├── telegram.py       # text, photo, and voice message delivery
│   └── voice.py          # MiMo TTS integration
├── utils/
│   ├── database.py       # SQLite CRUD
│   ├── nutrition.py      # USDA nutrition reference data
│   └── formatting.py     # pretty-print macros and stats
└── data/nutrition.db     # pre-built nutrition lookup table
```

## What's Next

- Body photo progress tracking (visual diffs over weeks)
- Barcode scanning for packaged foods
- Wearable integration (Apple Watch, Fitbit)
- Meal planning with auto-generated grocery lists
- Workout plan generation based on goals and history

---

MIT License

Built by [@spengeboob](https://github.com/spengeboob) · Powered by [Xiaomi MiMo](https://mimo.xiaomi.com/)
