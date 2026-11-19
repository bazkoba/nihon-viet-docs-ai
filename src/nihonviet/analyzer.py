"""AI analysis of a Japanese document, explained in Vietnamese, using Claude.

The offline rule report is passed to the model as grounding so that dates,
deadlines and red flags found deterministically are never contradicted.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from .rules import RuleReport, analyze_offline

MODEL = "claude-opus-5-5"

SYSTEM_PROMPT = """\
Bạn là trợ lý giúp người Việt Nam đang sống và làm việc tại Nhật Bản hiểu giấy tờ tiếng Nhật
(giấy tờ nhập cư, thuế, bảo hiểm, hợp đồng lao động, hợp đồng thuê nhà, hóa đơn).

Người đọc thường là thực tập sinh hoặc kỹ sư, tiếng Nhật chưa tốt. Hãy:
- Giải thích bằng tiếng Việt đơn giản, dễ hiểu, không dùng từ chuyên ngành nếu không cần.
- Nói rõ người đọc PHẢI LÀM GÌ, trước NGÀY NÀO, mang theo GÌ, nộp Ở ĐÂU.
- Ngày tháng luôn ghi theo dương lịch (dd/mm/yyyy); dữ liệu ngày đã được hệ thống chuyển đổi từ
  lịch Nhật (令和...) và là chính xác — đừng tự tính lại khác đi.
- Chỉ ra điều khoản bất lợi hoặc có dấu hiệu trái luật lao động Nhật, nhưng không phóng đại.
- Nếu tài liệu không đủ thông tin, nói rõ là không chắc thay vì đoán.
Đây không phải tư vấn pháp lý; với vấn đề nghiêm trọng hãy khuyên liên hệ cơ quan hỗ trợ
(ví dụ: 外国人技能実習機構, 労働基準監督署, hoặc luật sư).
"""


class ActionItem(BaseModel):
    task_vi: str = Field(description="Việc cần làm, tiếng Việt")
    deadline: str | None = Field(description="Hạn chót dạng YYYY-MM-DD, hoặc null")
    where: str | None = Field(description="Nơi nộp / liên hệ, hoặc null")
    items_to_bring: list[str] = Field(description="Giấy tờ / đồ cần mang theo")


class Risk(BaseModel):
    level: Literal["low", "medium", "high"]
    quote_ja: str = Field(description="Đoạn văn gốc tiếng Nhật liên quan")
    explanation_vi: str


class DocumentAnalysis(BaseModel):
    title_ja: str
    title_vi: str
    sender: str | None
    summary_vi: str = Field(description="Tóm tắt 2-4 câu tiếng Việt")
    translation_vi: str = Field(description="Bản dịch tiếng Việt đầy đủ, giữ cấu trúc")
    actions: list[ActionItem]
    risks: list[Risk]
    reply_draft_ja: str | None = Field(description="Bản nháp trả lời / hỏi lại bằng tiếng Nhật lịch sự nếu cần, hoặc null")


def _grounding(report: RuleReport, today: date) -> str:
    lines = [f"Hôm nay: {today.isoformat()}", f"Loại tài liệu (rule-based): {report.doc_type_vi}"]
    if report.dates:
        lines.append("Ngày tìm thấy (đã đổi sang dương lịch):")
        lines += [f"- {d.source} = {d.value.isoformat()}" for d in report.dates]
    if report.deadlines:
        lines.append("Hạn chót phát hiện:")
        lines += [f"- {d.when.isoformat()} (còn {d.days_left} ngày): {d.context}" for d in report.deadlines]
    if report.red_flags:
        lines.append("Cảnh báo rule-based:")
        lines += [f"- {f}" for f in report.red_flags]
    return "\n".join(lines)


def analyze(text: str, today: date | None = None, client=None) -> tuple[RuleReport, DocumentAnalysis]:
    """Analyze ``text`` with Claude. Requires the ``anthropic`` package and credentials."""
    import anthropic

    today = today or date.today()
    report = analyze_offline(text, today)
    client = client or anthropic.Anthropic()

    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"<grounding>\n{_grounding(report, today)}\n</grounding>\n\n"
                    f"<document>\n{text}\n</document>\n\n"
                    "Hãy phân tích tài liệu trên."
                ),
            }
        ],
        output_format=DocumentAnalysis,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to analyze this document.")
    if response.parsed_output is None:
        raise RuntimeError(f"No structured output (stop_reason={response.stop_reason}).")
    return report, response.parsed_output
