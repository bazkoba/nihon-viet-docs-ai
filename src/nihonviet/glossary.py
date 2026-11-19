"""Japanese administrative / workplace terms with Vietnamese explanations.

Hand-curated for Vietnamese technical intern trainees (技能実習生), specified
skilled workers (特定技能) and engineers living in Japan.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    ja: str
    reading: str
    vi: str
    note: str = ""


TERMS: list[Term] = [
    # Immigration / residence
    Term("在留カード", "ざいりゅうカード", "Thẻ cư trú", "Luôn mang theo người; mất phải báo trong 14 ngày."),
    Term("在留資格", "ざいりゅうしかく", "Tư cách lưu trú (loại visa)"),
    Term("在留期間更新許可申請", "ざいりゅうきかんこうしんきょかしんせい", "Đơn xin gia hạn thời gian lưu trú", "Nộp được từ 3 tháng trước ngày hết hạn."),
    Term("在留資格変更許可申請", "ざいりゅうしかくへんこうきょかしんせい", "Đơn xin đổi tư cách lưu trú"),
    Term("在留期限", "ざいりゅうきげん", "Ngày hết hạn lưu trú"),
    Term("資格外活動許可", "しかくがいかつどうきょか", "Giấy phép hoạt động ngoài tư cách lưu trú (làm thêm)", "Du học sinh tối đa 28 giờ/tuần."),
    Term("再入国許可", "さいにゅうこくきょか", "Giấy phép tái nhập cảnh"),
    Term("出入国在留管理庁", "しゅつにゅうこくざいりゅうかんりちょう", "Cục Quản lý Xuất nhập cảnh và Lưu trú"),
    Term("技能実習", "ぎのうじっしゅう", "Thực tập kỹ năng (thực tập sinh)"),
    Term("特定技能", "とくていぎのう", "Kỹ năng đặc định"),
    Term("技術・人文知識・国際業務", "ぎじゅつ・じんぶんちしき・こくさいぎょうむ", "Visa kỹ sư / nhân văn / quốc tế (visa kỹ sư)"),
    Term("永住許可", "えいじゅうきょか", "Giấy phép vĩnh trú"),
    # Municipal
    Term("住民票", "じゅうみんひょう", "Phiếu cư trú"),
    Term("転入届", "てんにゅうとどけ", "Đăng ký chuyển đến", "Trong vòng 14 ngày sau khi chuyển nhà."),
    Term("転出届", "てんしゅつとどけ", "Đăng ký chuyển đi"),
    Term("マイナンバー", "マイナンバー", "Mã số cá nhân (My Number)"),
    Term("市役所", "しやくしょ", "Tòa thị chính"),
    Term("区役所", "くやくしょ", "Văn phòng quận"),
    # Tax / insurance / pension
    Term("住民税", "じゅうみんぜい", "Thuế cư trú", "Tính theo thu nhập năm trước."),
    Term("所得税", "しょとくぜい", "Thuế thu nhập"),
    Term("源泉徴収票", "げんせんちょうしゅうひょう", "Phiếu khấu trừ thuế tại nguồn", "Cần khi gia hạn visa, xin vĩnh trú, khai thuế."),
    Term("確定申告", "かくていしんこく", "Quyết toán thuế (tự khai)"),
    Term("年末調整", "ねんまつちょうせい", "Điều chỉnh thuế cuối năm (công ty làm)"),
    Term("納税証明書", "のうぜいしょうめいしょ", "Giấy chứng nhận nộp thuế"),
    Term("課税証明書", "かぜいしょうめいしょ", "Giấy chứng nhận mức thuế"),
    Term("国民健康保険", "こくみんけんこうほけん", "Bảo hiểm y tế quốc dân"),
    Term("社会保険", "しゃかいほけん", "Bảo hiểm xã hội (qua công ty)"),
    Term("厚生年金", "こうせいねんきん", "Lương hưu phúc lợi (qua công ty)"),
    Term("国民年金", "こくみんねんきん", "Lương hưu quốc dân"),
    Term("脱退一時金", "だったいいちじきん", "Tiền hoàn trả lương hưu một lần", "Xin trong vòng 2 năm sau khi rời Nhật."),
    Term("督促状", "とくそくじょう", "Thư đôn đốc nộp tiền", "Quan trọng! Chậm nộp sẽ bị phạt và ảnh hưởng gia hạn visa."),
    Term("延滞金", "えんたいきん", "Tiền phạt chậm nộp"),
    Term("納付書", "のうふしょ", "Phiếu nộp tiền"),
    Term("納期限", "のうきげん", "Hạn nộp tiền"),
    # Employment
    Term("雇用契約書", "こようけいやくしょ", "Hợp đồng lao động"),
    Term("労働条件通知書", "ろうどうじょうけんつうちしょ", "Thông báo điều kiện lao động"),
    Term("給与明細", "きゅうよめいさい", "Bảng lương chi tiết"),
    Term("基本給", "きほんきゅう", "Lương cơ bản"),
    Term("残業代", "ざんぎょうだい", "Tiền làm thêm giờ"),
    Term("控除", "こうじょ", "Khoản khấu trừ"),
    Term("手取り", "てどり", "Lương thực nhận"),
    Term("有給休暇", "ゆうきゅうきゅうか", "Nghỉ phép có lương"),
    Term("試用期間", "しようきかん", "Thời gian thử việc"),
    Term("退職届", "たいしょくとどけ", "Đơn xin nghỉ việc"),
    Term("解雇", "かいこ", "Sa thải", "Công ty phải báo trước ít nhất 30 ngày hoặc trả tiền thay thế."),
    Term("違約金", "いやくきん", "Tiền phạt vi phạm hợp đồng", "Điều khoản phạt khi nghỉ việc thường trái Luật Lao động (労働基準法第16条)."),
    Term("雇用保険", "こようほけん", "Bảo hiểm thất nghiệp"),
    Term("離職票", "りしょくひょう", "Phiếu nghỉ việc (để nhận trợ cấp thất nghiệp)"),
    # Housing / money
    Term("賃貸借契約書", "ちんたいしゃくけいやくしょ", "Hợp đồng thuê nhà"),
    Term("敷金", "しききん", "Tiền đặt cọc"),
    Term("礼金", "れいきん", "Tiền lễ (không hoàn lại)"),
    Term("更新料", "こうしんりょう", "Phí gia hạn hợp đồng thuê"),
    Term("原状回復", "げんじょうかいふく", "Khôi phục nguyên trạng khi trả nhà"),
    Term("連帯保証人", "れんたいほしょうにん", "Người bảo lãnh liên đới"),
    Term("請求書", "せいきゅうしょ", "Hóa đơn yêu cầu thanh toán"),
    Term("領収書", "りょうしゅうしょ", "Biên lai"),
    Term("見積書", "みつもりしょ", "Báo giá"),
    Term("振込", "ふりこみ", "Chuyển khoản"),
    Term("口座振替", "こうざふりかえ", "Trích nợ tự động từ tài khoản"),
    Term("印鑑", "いんかん", "Con dấu cá nhân"),
    Term("署名", "しょめい", "Chữ ký"),
    Term("期限", "きげん", "Thời hạn"),
    Term("必着", "ひっちゃく", "Phải đến nơi trước (hạn chót nhận)"),
    Term("提出", "ていしゅつ", "Nộp (hồ sơ)"),
]

_BY_JA = {t.ja: t for t in TERMS}


def lookup(ja: str) -> Term | None:
    return _BY_JA.get(ja)


def find_terms(text: str) -> list[Term]:
    """Return glossary terms that appear in ``text``.

    Longer terms win: if 在留期間更新許可申請 appears, the shorter 在留 terms
    contained inside that same span are not reported again.
    """
    hits: list[tuple[int, Term]] = []
    covered: list[range] = []
    for term in sorted(TERMS, key=lambda t: len(t.ja), reverse=True):
        start = text.find(term.ja)
        while start != -1:
            span = range(start, start + len(term.ja))
            if not any(start in r and span[-1] in r for r in covered):
                hits.append((start, term))
                covered.append(span)
                break
            start = text.find(term.ja, start + 1)
    seen: set[str] = set()
    result = []
    for _, term in sorted(hits, key=lambda h: h[0]):
        if term.ja not in seen:
            seen.add(term.ja)
            result.append(term)
    return result
