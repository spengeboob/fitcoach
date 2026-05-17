"""Output formatting utilities."""

from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))


def format_progress_bar(current: float, target: float, width: int = 10) -> str:
    """Format a text progress bar."""
    if target == 0:
        return "░" * width
    filled = min(width, int(current / target * width))
    return "█" * filled + "░" * (width - filled)


def format_weight_change(change_kg: float) -> str:
    """Format weight change with emoji."""
    if change_kg > 0:
        return f"📈 +{change_kg:.1f}kg"
    elif change_kg < 0:
        return f"📉 {change_kg:.1f}kg"
    return "➡️ No change"
