from datetime import datetime
from typing import Optional

def normalize_date(date_str: str) -> Optional[str]:
    if not date_str:
        return None

    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).date().isoformat()
        except ValueError:
            continue

    return None


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None