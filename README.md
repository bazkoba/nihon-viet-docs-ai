# nihon-viet-docs-ai 🇯🇵➡️🇻🇳

**Trợ lý AI giúp người Việt ở Nhật đọc hiểu giấy tờ tiếng Nhật.**
Covers visa documents, tax, insurance, labor contracts, rental contracts and invoices.

日本で暮らすベトナム人のための、日本語書類（在留資格・税金・保険・雇用契約・賃貸契約・請求書）を
ベトナム語でわかりやすく解説する AI アシスタントです。

---

## Vì sao? / なぜ？ / Why?

- Có **khoảng 60 vạn người Việt** đang sống tại Nhật, phần lớn là thực tập sinh kỹ năng, lao động kỹ năng đặc định và kỹ sư.
- Giấy tờ hành chính Nhật dùng **lịch Nhật (令和7年…)**, nhiều từ Hán khó và thời hạn rất nghiêm. Bỏ lỡ một thư đôn đốc thuế (督促状) có thể ảnh hưởng tới **việc gia hạn visa**.
- Google Translate chỉ dịch chữ. Nó không cho biết **phải làm gì, trước ngày nào, điều khoản nào trái luật**.

## Tính năng / 機能 / Features

| | Offline (không cần API key) | AI (Claude) |
|---|---|---|
| Đổi ngày lịch Nhật → dương lịch (令和 / 平成 / R7.3.31 / chữ số toàn góc) | ✅ | ✅ |
| Phát hiện **hạn chót** và số ngày còn lại | ✅ | ✅ |
| Phân loại tài liệu (visa, thuế, bảo hiểm, lao động, nhà, hóa đơn) | ✅ | ✅ |
| Cảnh báo **dấu hiệu trái luật** (giữ hộ chiếu, phạt tiền khi nghỉ việc, 差押…) | ✅ | ✅ |
| Từ điển ~65 thuật ngữ hành chính Nhật–Việt | ✅ | ✅ |
| Dịch đầy đủ sang tiếng Việt dễ hiểu | | ✅ |
| Danh sách **việc cần làm**: nộp gì, ở đâu, mang theo gì | | ✅ |
| Soạn sẵn thư trả lời bằng tiếng Nhật lịch sự | | ✅ |

The offline engine's dates and deadlines go into the AI prompt as grounding, so the model never recomputes Japanese era dates on its own.

## Cài đặt / Install

```bash
git clone https://github.com/bazkoba/nihon-viet-docs-ai.git
cd nihon-viet-docs-ai
pip install -e ".[ai,dev]"
```

## Sử dụng / Usage

```bash
# Đổi ngày
nihonviet date 令和7年12月15日
# → 15/12/2025

# Phân tích offline
nihonviet check examples/zeikin_tokusoku.txt

# Phân tích bằng AI (dịch + giải thích + việc cần làm)
export ANTHROPIC_API_KEY=...
nihonviet check examples/koyou_keiyaku.txt --ai
```

Ví dụ kết quả offline với thư đôn đốc thuế cư trú:

```
📄 Loại tài liệu: Thuế

⏰ HẠN CHÓT:
  • 15/12/2025 (令和7年12月15日) — còn 20 ngày

💴 Số tiền: 18,500円, 1,200円

⚠️  CẢNH BÁO:
  • Thư đôn đốc: bạn đang nợ tiền (thuế/bảo hiểm). Nộp ngay để tránh ảnh hưởng gia hạn visa.
  • Có tiền phạt chậm nộp. Càng để lâu càng tăng.
  • CẢNH BÁO: có thể bị tịch thu tài sản / tài khoản. Liên hệ cơ quan ngay.
```

### Dùng như thư viện / As a library

```python
from nihonviet import parse_date, analyze_offline

parse_date("R7.3.31")            # datetime.date(2025, 3, 31)
report = analyze_offline(text)
report.deadlines, report.red_flags
```

## Cấu trúc / Architecture

```
src/nihonviet/
├── wareki.py     # 和暦 ⇄ dương lịch, tìm ngày trong văn bản
├── glossary.py   # Từ điển thuật ngữ hành chính Nhật–Việt
├── rules.py      # Phân loại, hạn chót, số tiền, cờ đỏ (offline)
├── analyzer.py   # Claude (structured output) + grounding từ rules.py
└── cli.py        # Lệnh `nihonviet`
```

## Lộ trình / Roadmap

- [ ] OCR: chụp ảnh giấy tờ → văn bản (Claude vision)
- [ ] LINE bot. Đa số người Việt ở Nhật dùng LINE và Messenger.
- [ ] Web app cho điện thoại
- [ ] Nhắc hạn chót qua lịch / thông báo
- [ ] Mở rộng sang tiếng Indonesia, Nepal, Myanmar, Philippines

## Lưu ý / 免責事項 / Disclaimer

Đây là công cụ hỗ trợ đọc hiểu, **không phải tư vấn pháp lý**. Với vấn đề nghiêm trọng, hãy liên hệ
外国人技能実習機構 (OTIT), 労働基準監督署, hoặc luật sư.

## License

MIT
