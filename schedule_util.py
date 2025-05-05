from datetime import datetime

# SHOP HOURS
SHOP_OPEN  = datetime.strptime("08:00", "%H:%M").time()
SHOP_CLOSE = datetime.strptime("17:00", "%H:%M").time()

def clamp_availability(avail: str) -> tuple[str, str]:
    """
    Parse an "HH:MM-HH:MM" availability string
    and clamp the times to SHOP_OPEN–SHOP_CLOSE.
    Returns (start_str, end_str).
    """
    try:
        start_str, end_str = [s.strip() for s in avail.split("-")]
        start = datetime.strptime(start_str, "%H:%M").time()
        end   = datetime.strptime(end_str,   "%H:%M").time()
    except ValueError:
        # Fall back to full shop hours on bad input
        return SHOP_OPEN.strftime("%H:%M"), SHOP_CLOSE.strftime("%H:%M")

    # Clamp to shop hours
    if start < SHOP_OPEN:  start = SHOP_OPEN
    if end   > SHOP_CLOSE: end   = SHOP_CLOSE

    return start.strftime("%H:%M"), end.strftime("%H:%M")
