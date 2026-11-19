from datetime import date
from pathlib import Path

import pytest

from nihonviet.cli import main
from nihonviet.glossary import find_terms
from nihonviet.rules import analyze_offline, classify, find_amounts
from nihonviet.wareki import era_to_gregorian, find_dates, parse_date

EXAMPLES = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("令和7年3月31日", date(2025, 3, 31)),
        ("令和元年5月1日", date(2019, 5, 1)),
        ("平成31年4月30日", date(2019, 4, 30)),
        ("昭和64年1月7日", date(1989, 1, 7)),
        ("令和７年１２月１５日", date(2025, 12, 15)),  # full-width digits
        ("R7.3.31", date(2025, 3, 31)),
        ("H31/4/30", date(2019, 4, 30)),
        ("2025年3月31日", date(2025, 3, 31)),
        ("2025/03/31", date(2025, 3, 31)),
    ],
)
def test_parse_date(text, expected):
    assert parse_date(text) == expected


def test_era_year():
    assert era_to_gregorian("令和", 1) == 2019
    assert era_to_gregorian("R", 8) == 2026
    with pytest.raises(ValueError):
        era_to_gregorian("X", 1)


def test_invalid_dates_are_skipped():
    assert find_dates("令和元年1月1日") == []  # before Reiwa started
    assert find_dates("令和7年2月30日") == []


def test_dates_not_double_counted():
    dates = find_dates("期限は令和7年3月31日（2025年3月31日）です")
    assert [d.value for d in dates] == [date(2025, 3, 31), date(2025, 3, 31)]
    assert dates[0].source.startswith("令和")


def test_classify():
    assert classify("住民税の納税通知書")[0] == "tax"
    assert classify("在留期間更新許可申請")[0] == "residence"
    assert classify("こんにちは")[0] == "other"


def test_amounts():
    assert find_amounts("合計 18,500円 と ￥1,200") == [18500, 1200]


def test_glossary_prefers_longest():
    terms = [t.ja for t in find_terms("在留期間更新許可申請を提出してください")]
    assert "在留期間更新許可申請" in terms
    assert "提出" in terms


def test_tax_reminder_example():
    r = analyze_offline((EXAMPLES / "zeikin_tokusoku.txt").read_text(encoding="utf-8"), today=date(2025, 11, 25))
    assert r.doc_type == "tax"
    assert [d.when for d in r.deadlines] == [date(2025, 12, 15)]
    assert r.deadlines[0].days_left == 20
    assert 18500 in r.amounts_yen
    assert any("đôn đốc" in f for f in r.red_flags)
    assert any("tịch thu" in f for f in r.red_flags)


def test_contract_example_flags_illegal_clauses():
    r = analyze_offline((EXAMPLES / "koyou_keiyaku.txt").read_text(encoding="utf-8"), today=date(2025, 12, 1))
    assert r.doc_type == "employment"
    assert date(2025, 12, 10) in [d.when for d in r.deadlines]
    assert any("hộ chiếu" in f for f in r.red_flags)
    assert any("phạt" in f for f in r.red_flags)


def test_cli_date(capsys):
    assert main(["date", "令和8年1月1日"]) == 0
    assert capsys.readouterr().out.strip() == "01/01/2026"


def test_cli_check(capsys):
    assert main(["check", str(EXAMPLES / "zeikin_tokusoku.txt"), "--today", "2025-11-25"]) == 0
    out = capsys.readouterr().out
    assert "15/12/2025" in out
    assert "còn 20 ngày" in out
