"""Japanese era (和暦) date parsing.

Japanese official documents (在留カード, 住民税, 年金, 契約書 ...) almost always write
dates in the imperial era format, e.g. ``令和7年3月31日`` or ``R7.3.31``.
Vietnamese residents frequently misread these, which leads to missed deadlines.
This module converts them to Gregorian ``datetime.date`` objects.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date

# (era name, romaji initial, first Gregorian year, first day of the era)
ERAS: list[tuple[str, str, date]] = [
    ("令和", "R", date(2019, 5, 1)),
    ("平成", "H", date(1989, 1, 8)),
    ("昭和", "S", date(1926, 12, 25)),
    ("大正", "T", date(1912, 7, 30)),
    ("明治", "M", date(1868, 1, 25)),
]

_ERA_BY_NAME = {name: start for name, _, start in ERAS}
_ERA_BY_INITIAL = {initial: start for _, initial, start in ERAS}

_KANJI_ERA = "|".join(name for name, _, _ in ERAS)

# 令和7年3月31日 / 令和元年5月1日 / 令和 7 年 3 月 31 日
_KANJI_PATTERN = re.compile(
    rf"(?P<era>{_KANJI_ERA})\s*(?P<year>元|\d{{1,2}})\s*年\s*(?P<month>\d{{1,2}})\s*月\s*(?P<day>\d{{1,2}})\s*日"
)
# R7.3.31 / R07/03/31 / H31-4-30
_INITIAL_PATTERN = re.compile(
    r"(?<![A-Za-z])(?P<era>[RHSTM])\s*(?P<year>\d{1,2})[./\-](?P<month>\d{1,2})[./\-](?P<day>\d{1,2})"
)
# 2025年3月31日 / 2025/3/31 / 2025-03-31
_SEIREKI_PATTERN = re.compile(
    r"(?P<year>(?:19|20)\d{2})\s*(?:年|/|-|\.)\s*(?P<month>\d{1,2})\s*(?:月|/|-|\.)\s*(?P<day>\d{1,2})\s*日?"
)


@dataclass(frozen=True)
class FoundDate:
    """A date found in a document together with the exact source text."""

    value: date
    source: str
    start: int
    end: int


def normalize(text: str) -> str:
    """Convert full-width digits/letters (２０２５, Ｒ７) to half-width."""
    return unicodedata.normalize("NFKC", text)


def era_to_gregorian(era: str, era_year: int) -> int:
    """Return the Gregorian year for ``era`` year ``era_year`` (1 == 元年)."""
    start = _ERA_BY_NAME.get(era) or _ERA_BY_INITIAL.get(era.upper())
    if start is None:
        raise ValueError(f"unknown era: {era!r}")
    if era_year < 1:
        raise ValueError("era year must be >= 1")
    return start.year + era_year - 1


def _build(era: str | None, year: str, month: str, day: str) -> date | None:
    y = 1 if year == "元" else int(year)
    try:
        gyear = era_to_gregorian(era, y) if era else y
        result = date(gyear, int(month), int(day))
    except ValueError:
        return None
    if era:
        start = _ERA_BY_NAME.get(era) or _ERA_BY_INITIAL[era]
        if result < start:
            return None  # e.g. 令和1年1月1日 did not exist
    return result


def find_dates(text: str) -> list[FoundDate]:
    """Find every era or Gregorian date in ``text``, in order of appearance."""
    norm = normalize(text)
    found: list[FoundDate] = []
    taken: list[range] = []

    for pattern, has_era in ((_KANJI_PATTERN, True), (_INITIAL_PATTERN, True), (_SEIREKI_PATTERN, False)):
        for m in pattern.finditer(norm):
            if any(m.start() in r or (m.end() - 1) in r for r in taken):
                continue
            value = _build(m.group("era") if has_era else None, m.group("year"), m.group("month"), m.group("day"))
            if value is None:
                continue
            found.append(FoundDate(value, m.group(0), m.start(), m.end()))
            taken.append(range(m.start(), m.end()))

    return sorted(found, key=lambda d: d.start)


def parse_date(text: str) -> date:
    """Parse a single date string such as ``令和7年3月31日``."""
    dates = find_dates(text)
    if not dates:
        raise ValueError(f"no date found in {text!r}")
    return dates[0].value
