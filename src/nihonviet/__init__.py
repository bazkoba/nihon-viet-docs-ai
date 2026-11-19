"""nihonviet — help Vietnamese people in Japan understand Japanese documents."""

from .rules import analyze_offline
from .wareki import find_dates, parse_date

__all__ = ["analyze_offline", "find_dates", "parse_date"]
__version__ = "0.1.0"
