"""Offline, rule-based analysis: document type, deadlines and red flags.

Works without any API key, so the tool is still useful (and testable) offline.
The LLM analyzer in :mod:`nihonviet.analyzer` builds on these results.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

from .glossary import Term, find_terms
from .wareki import FoundDate, find_dates, normalize

DOC_TYPES: dict[str, tuple[str, list[str]]] = {
    # key: (Vietnamese label, keywords)
    "residence": ("Giấy tờ lưu trú / visa", ["在留", "入管", "出入国", "在留カード", "更新許可"]),
    "tax": ("Thuế", ["住民税", "市民税", "県民税", "都民税", "所得税", "納税", "課税", "確定申告", "源泉徴収", "地方税", "市税"]),
    "insurance_pension": ("Bảo hiểm / lương hưu", ["健康保険", "年金", "保険料", "社会保険"]),
    "employment": ("Hợp đồng / lao động", ["雇用契約", "労働条件", "給与", "就業規則", "退職", "解雇", "残業"]),
    "housing": ("Nhà ở", ["賃貸", "敷金", "礼金", "家賃", "管理会社", "原状回復"]),
    "invoice": ("Hóa đơn / thanh toán", ["請求書", "ご請求", "振込", "お支払", "領収書", "見積"]),
}

# words that, when near a date, mean "this is a deadline"
_DEADLINE_HINTS = ["期限", "まで", "必着", "締切", "締め切り", "迄", "以内", "期日", "納期"]

RED_FLAGS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"督促"), "Thư đôn đốc: bạn đang nợ tiền (thuế/bảo hiểm). Nộp ngay để tránh ảnh hưởng gia hạn visa."),
    (re.compile(r"延滞金"), "Có tiền phạt chậm nộp. Càng để lâu càng tăng."),
    (re.compile(r"差押|差し押さえ"), "CẢNH BÁO: có thể bị tịch thu tài sản / tài khoản. Liên hệ cơ quan ngay."),
    (re.compile(r"違約金|罰金"), "Có điều khoản tiền phạt. Phạt khi nghỉ việc thường trái luật (労働基準法第16条)."),
    (re.compile(r"パスポート.{0,10}(預か|保管)"), "Công ty giữ hộ chiếu là trái luật. Bạn có quyền tự giữ."),
    (re.compile(r"在留カード.{0,10}(預か|保管)"), "Công ty giữ thẻ cư trú là trái luật."),
    (re.compile(r"不許可"), "Hồ sơ bị TỪ CHỐI. Đọc kỹ lý do và thời hạn rời Nhật / nộp lại."),
    (re.compile(r"出頭"), "Bạn được yêu cầu có mặt trực tiếp. Đừng bỏ qua."),
    (re.compile(r"退去強制|強制退去"), "CẢNH BÁO: liên quan trục xuất. Hãy tìm luật sư / hỗ trợ ngay."),
]


@dataclass
class Deadline:
    when: date
    source: str
    context: str
    days_left: int


@dataclass
class RuleReport:
    doc_type: str
    doc_type_vi: str
    dates: list[FoundDate]
    deadlines: list[Deadline]
    red_flags: list[str]
    terms: list[Term]
    amounts_yen: list[int] = field(default_factory=list)


def classify(text: str) -> tuple[str, str]:
    scores = {key: sum(text.count(k) for k in kws) for key, (_, kws) in DOC_TYPES.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "other", "Khác"
    return best, DOC_TYPES[best][0]


def _context(text: str, start: int, end: int, width: int = 25) -> str:
    return text[max(0, start - width): end + width].replace("\n", " ").strip()


def find_deadlines(text: str, today: date | None = None) -> list[Deadline]:
    today = today or date.today()
    norm = normalize(text)
    result = []
    for d in find_dates(norm):
        window = norm[max(0, d.start - 15): d.end + 12]
        if any(h in window for h in _DEADLINE_HINTS):
            result.append(Deadline(d.value, d.source, _context(norm, d.start, d.end), (d.value - today).days))
    return result


_YEN = re.compile(r"(?:¥|￥)\s*([\d,]+)|([\d,]+)\s*円")


def find_amounts(text: str) -> list[int]:
    out = []
    for m in _YEN.finditer(normalize(text)):
        raw = (m.group(1) or m.group(2)).replace(",", "")
        if raw.isdigit():
            out.append(int(raw))
    return out


def analyze_offline(text: str, today: date | None = None) -> RuleReport:
    norm = normalize(text)
    key, label = classify(norm)
    return RuleReport(
        doc_type=key,
        doc_type_vi=label,
        dates=find_dates(norm),
        deadlines=find_deadlines(norm, today),
        red_flags=[msg for pat, msg in RED_FLAGS if pat.search(norm)],
        terms=find_terms(norm),
        amounts_yen=find_amounts(norm),
    )
