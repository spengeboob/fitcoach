"""Food photo analyzer using MiMo Vision."""

import json
import logging
import httpx

logger = logging.getLogger("fitcoach.food")


class FoodAnalyzer:
    """Analyze food photos using MiMo's multimodal vision."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def analyze_photo(self, photo_path: str) -> dict | None:
        """Analyze a food photo and return nutritional data."""
        import base64

        with open(photo_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        prompt = """Analyze this food photo. Return a JSON object with:
{
  "dishes": [
    {
      "name": "dish name",
      "portion": "estimated portion size",
      "calories": estimated_kcal,
      "protein_g": grams,
      "carbs_g": grams,
      "fat_g": grams,
      "fiber_g": grams
    }
  ],
  "total": {
    "calories": sum,
    "protein_g": sum,
    "carbs_g": sum,
    "fat_g": sum,
    "fiber_g": sum
  },
  "notes": "brief nutritional observation"
}
Return ONLY the JSON, no other text."""

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
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_b64}"
                                        },
                                    },
                                ],
                            }
                        ],
                        "max_tokens": 1000,
                    },
                    timeout=30,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    # Parse JSON from response
                    return json.loads(content.strip("` \n").replace("json\n", "", 1))
                else:
                    logger.error("MiMo Vision API error: %s", resp.text)
                    return None

        except Exception as e:
            logger.error("Food analysis error: %s", e)
            return None

    def format_analysis(self, analysis: dict) -> str:
        """Format food analysis as readable message."""
        total = analysis.get("total", {})
        dishes = analysis.get("dishes", [])
        notes = analysis.get("notes", "")

        lines = ["📸 <b>Meal logged!</b>", ""]

        for dish in dishes:
            lines.append(f"🍽️ {dish['name']} ({dish.get('portion', '')})")
            lines.append(f"   • {dish.get('calories', 0)} kcal")
            lines.append(f"   • P: {dish.get('protein_g', 0)}g | C: {dish.get('carbs_g', 0)}g | F: {dish.get('fat_g', 0)}g")
            lines.append("")

        lines.append(f"📊 <b>Total:</b> {total.get('calories', 0)} kcal")
        lines.append(f"   Protein: {total.get('protein_g', 0)}g")
        lines.append(f"   Carbs: {total.get('carbs_g', 0)}g")
        lines.append(f"   Fat: {total.get('fat_g', 0)}g")

        if notes:
            lines.extend(["", f"💡 {notes}"])

        return "\n".join(lines)

    def format_daily_progress(self, daily: dict, config) -> str:
        """Format daily macro progress."""
        cal_pct = (daily.get("calories", 0) / config.calorie_target * 100) if config.calorie_target else 0
        pro_pct = (daily.get("protein_g", 0) / config.protein_target_g * 100) if config.protein_target_g else 0

        lines = [
            "",
            "📈 <b>Today's Progress:</b>",
            f"   Calories: {daily.get('calories', 0):,} / {config.calorie_target:,} ({cal_pct:.0f}%)",
            f"   Protein: {daily.get('protein_g', 0):.0f}g / {config.protein_target_g}g ({pro_pct:.0f}%)",
        ]

        if pro_pct < 70:
            lines.append("💡 Protein is low — consider adding a protein source to your next meal.")

        return "\n".join(lines)

    async def suggest_meal(self, daily: dict, config) -> str:
        """Suggest a meal based on remaining macros."""
        remaining = {
            "calories": max(0, config.calorie_target - daily.get("calories", 0)),
            "protein_g": max(0, config.protein_target_g - daily.get("protein_g", 0)),
            "carbs_g": max(0, config.carb_target_g - daily.get("carbs_g", 0)),
            "fat_g": max(0, config.fat_target_g - daily.get("fat_g", 0)),
        }

        prompt = f"""Suggest a meal that fits these remaining daily macros:
- Calories: ~{remaining['calories']} kcal
- Protein: ~{remaining['protein_g']}g
- Carbs: ~{remaining['carbs_g']}g
- Fat: ~{remaining['fat_g']}g

Give 2-3 practical meal ideas with approximate macros. Keep it concise and actionable."""

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
                        "max_tokens": 500,
                    },
                    timeout=15,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                return "Couldn't generate suggestion right now."

        except Exception as e:
            logger.error("Meal suggestion error: %s", e)
            return "Error generating meal suggestion."
