# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how many percent of the service interval have been used.

    Uses true (float) division so a car at 14,900 of 15,000 km
    correctly reports ~99.3 % rather than 0 %.
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has used >= WARN_AT_PERCENT of its service interval.

    A car with no last_service_km reading is left un-flagged: we cannot
    calculate wear without a baseline, so we do not guess.
    """
    if "last_service_km" not in car:
        return False
    km_since = car["odometer"] - car["last_service_km"]
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that is due for service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
