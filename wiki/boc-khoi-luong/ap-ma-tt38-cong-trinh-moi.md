---
title: Áp mã định mức TT 38/2026 khi bóc khối lượng công trình xây mới
type: rule
topics: [dinh-muc, du-toan, boc-khoi-luong]
status: confirmed
source: Tra tập định mức CV 9947/BXD-VPB (phụ lục thay thế TT 38/2026/TT-BXD), bản PDF có chữ, trong phiên bóc khối lượng 11/2026
updated: 2026-11-05
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (05/11/2026)
---

# Áp mã định mức TT 38/2026 khi bóc khối lượng công trình xây mới

## Quy tắc

- **Mã đầy đủ = mã dòng + mã cột.** Bảng in mã dòng (ví dụ `AF.322`) và số cột ở cuối bảng (`10`, `30`…). Mã đầy đủ là `AF.32210`, `AF.32230`. Văn bản trích từ PDF hay làm lệch cột: mở ảnh trang để đối chiếu, chưa đối chiếu thì ghi độ tin cậy "cần đối chiếu PDF".
- **Công trình mới không nhân hệ số sửa chữa.** Hệ số VL×1,02, NC×1,15, M×1,05 chỉ dùng khi lấy mã xây mới cho công tác sửa chữa.
- **Ghi số trang PDF** (thứ tự trong file, không phải số in ở chân trang) cạnh mỗi mã.
- Định mức lắp dựng cửa, vách kính, thiết bị **không gồm vật tư chính**: tách dòng vật tư theo báo giá hoặc lập sheet phân tích đơn giá.
- Không có mã (tay vịn WC người khuyết tật, louver, vách ngăn WC compact, cửa thang máy) → định mức tự lập vận dụng mã gần nhất, hoặc báo giá trọn gói; ghi rõ "tự lập" / "báo giá".

## Mã hay dùng (xây mới, cao ≤ 6 m trừ khi ghi khác)

| Công tác | Mã | Đơn vị | Ghi chú |
|---|---|---|---|
| Bê tông cột ≤ 0,1 m², đổ bằng bơm | AF.32210 | m³ | cần cẩu: AF.22210 |
| Bê tông cột > 0,1 m², đổ bằng bơm | AF.32230 | m³ | cần cẩu: AF.22250 |
| Bê tông xà dầm, giằng, sàn, đổ bằng bơm | AF.32310 | m³ | |
| Ván khuôn cột vuông, chữ nhật, ván phủ phim, cao ≤ 28 m | AF.89141 | 100 m² | gỗ: AF.81132 |
| Ván khuôn xà dầm, giằng, ván phủ phim, cao ≤ 28 m | AF.89131 | 100 m² | |
| Ván khuôn sàn, ván phủ phim + khung thép hình + giáo, cao ≤ 28 m | AF.89411 | 100 m² | |
| Cốt thép cột Ø≤10 / Ø≤18 / Ø>18 | AF.61411 / 61421 / 61431 | tấn | |
| Cốt thép dầm Ø≤10 / Ø≤18 / Ø>18 | AF.61511 / 61521 / 61531 | tấn | |
| Cốt thép sàn Ø≤10 / Ø>10, cao ≤ 28 m | AF.61711 / 61721 | tấn | |
| Xây tường gạch đất sét nung dày ≤ 11 / ≤ 33 cm | AE.22110 / AE.22210 | m³ | |
| Ốp đá granit tự nhiên, chốt inox / keo dán | AK.32110 / AK.32120 | m² | ốp cột: NC × 1,25 |
| Lắp khuôn cửa đơn / cửa vào khuôn / cửa không khuôn | AH.31111 / AH.32111 / AH.32211 | m / m² / m² | |
| Lắp cửa khung sắt, khung nhôm | AI.63121 | m² | |
| Vách kính khung nhôm mặt tiền / trong nhà | AI.63231 / AI.63232 | m² | NC 0,50 / 0,30 công |
| Lắp xí bệt / chậu rửa 1 vòi / chậu tiểu nam | BB.91201 / BB.91101 / BB.91301 | bộ | chậu rửa đã gồm vòi |

Mã chưa đối chiếu bằng ảnh trang thì để độ tin cậy "cần đối chiếu PDF" trong sheet `MaDinhMuc` (xem [[bang-boc-khoi-luong-10-sheet]]).

> **Lưu ý khi dùng bảng trên:** các mã và hệ số sửa chữa (VL×1,02, NC×1,15, M×1,05) chưa được đối chiếu lại từng dòng với ảnh trang của văn bản gốc khi đưa vào kho này. Coi bảng là danh sách gợi ý để tìm nhanh, và kiểm lại từng mã (hao phí, cột điều kiện, đơn vị) bằng skill `tra-dinh-muc-du-toan` của launcher hoặc bằng chính văn bản trước khi dùng cho dự toán.
