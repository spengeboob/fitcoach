"""Nutrition database utilities."""

# Common food nutrition data per 100g (fallback when MiMo Vision isn't available)
NUTRITION_DB = {
    "rice": {"calories": 130, "protein_g": 2.7, "carbs_g": 28, "fat_g": 0.3},
    "chicken breast": {"calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6},
    "egg": {"calories": 155, "protein_g": 13, "carbs_g": 1.1, "fat_g": 11},
    "broccoli": {"calories": 34, "protein_g": 2.8, "carbs_g": 7, "fat_g": 0.4},
    "salmon": {"calories": 208, "protein_g": 20, "carbs_g": 0, "fat_g": 13},
    "tofu": {"calories": 76, "protein_g": 8, "carbs_g": 1.9, "fat_g": 4.8},
    "oats": {"calories": 389, "protein_g": 16.9, "carbs_g": 66, "fat_g": 6.9},
    "banana": {"calories": 89, "protein_g": 1.1, "carbs_g": 23, "fat_g": 0.3},
    "whey protein": {"calories": 120, "protein_g": 24, "carbs_g": 3, "fat_g": 1.5},
}


def lookup_food(name: str) -> dict | None:
    """Look up nutrition data for a food item."""
    name_lower = name.lower().strip()
    for key, value in NUTRITION_DB.items():
        if key in name_lower or name_lower in key:
            return value
    return None
