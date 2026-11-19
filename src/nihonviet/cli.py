"""Command line interface: ``nihonviet check document.txt``."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from .rules import RuleReport, analyze_offline
from .wareki import parse_date


def _print_report(r: RuleReport) -> None:
    print(f"📄 Loại tài liệu: {r.doc_type_vi}")
    if r.deadlines:
        print("\n⏰ HẠN CHÓT:")
        for d in r.deadlines:
            status = f"còn {d.days_left} ngày" if d.days_left >= 0 else f"ĐÃ QUÁ HẠN {-d.days_left} ngày"
            print(f"  • {d.when:%d/%m/%Y} ({d.source}) — {status}")
            print(f"    …{d.context}…")
    other = [d for d in r.dates if d.value not in {x.when for x in r.deadlines}]
    if other:
        print("\n📅 Ngày khác trong tài liệu:")
        for d in other:
            print(f"  • {d.source} → {d.value:%d/%m/%Y}")
    if r.amounts_yen:
        print("\n💴 Số tiền: " + ", ".join(f"{a:,}円" for a in r.amounts_yen))
    if r.red_flags:
        print("\n⚠️  CẢNH BÁO:")
        for f in r.red_flags:
            print(f"  • {f}")
    if r.terms:
        print("\n📖 Từ vựng:")
        for t in r.terms:
            note = f" — {t.note}" if t.note else ""
            print(f"  • {t.ja}（{t.reading}）: {t.vi}{note}")


def _print_ai(a) -> None:
    print(f"\n🤖 {a.title_vi}（{a.title_ja}）")
    if a.sender:
        print(f"Người gửi: {a.sender}")
    print(f"\n{a.summary_vi}")
    if a.actions:
        print("\n✅ Việc cần làm:")
        for act in a.actions:
            line = f"  • {act.task_vi}"
            if act.deadline:
                line += f" — trước {act.deadline}"
            if act.where:
                line += f" @ {act.where}"
            print(line)
            for item in act.items_to_bring:
                print(f"      - mang theo: {item}")
    if a.risks:
        print("\n🚩 Rủi ro:")
        for risk in a.risks:
            print(f"  • [{risk.level}] {risk.explanation_vi}\n      「{risk.quote_ja}」")
    print("\n🇻🇳 Bản dịch:\n" + a.translation_vi)
    if a.reply_draft_ja:
        print("\n✉️  Nháp trả lời (tiếng Nhật):\n" + a.reply_draft_ja)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="nihonviet", description="Đọc hiểu giấy tờ tiếng Nhật cho người Việt")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="Phân tích một tài liệu (file .txt hoặc '-' cho stdin)")
    c.add_argument("file")
    c.add_argument("--ai", action="store_true", help="Dùng Claude để dịch + giải thích (cần ANTHROPIC_API_KEY)")
    c.add_argument("--today", help="Ngày hôm nay (YYYY-MM-DD), mặc định là hôm nay")

    w = sub.add_parser("date", help="Đổi ngày lịch Nhật sang dương lịch, vd: 令和7年3月31日")
    w.add_argument("text")

    args = p.parse_args(argv)

    if args.cmd == "date":
        try:
            print(parse_date(args.text).strftime("%d/%m/%Y"))
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        return 0

    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    today = date.fromisoformat(args.today) if args.today else date.today()

    if args.ai:
        from .analyzer import analyze

        report, ai = analyze(text, today)
        _print_report(report)
        _print_ai(ai)
    else:
        _print_report(analyze_offline(text, today))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
