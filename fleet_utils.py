# fleet_utils.py
# Helper utilities for Vossberg Mobility fleet reporting.

MILES_PER_KM: float = 0.6213   # 1 km = 0.6213 miles (was 1.609, which is km-per-mile — inverted)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0 if the list is empty."""
    if not values:
        return 0.0
    return sum(values) / len(values)
