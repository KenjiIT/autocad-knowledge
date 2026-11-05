---
title: Cấu trúc chuẩn của bảng bóc khối lượng 10 sheet
type: howto
topics: [boc-khoi-luong, du-toan, excel]
status: confirmed
source: Rút ra từ bảng bóc khối lượng mẫu của một công trình cải tạo nhà ở và một bảng làm lại theo mẫu đó cho một tầng thương mại xây mới (phiên làm việc 11/2026)
updated: 2026-11-05
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (05/11/2026)
---

# Cấu trúc chuẩn của bảng bóc khối lượng 10 sheet

Bảng bóc khối lượng dùng làm chuẩn có **đủ 10 sheet, đúng thứ tự**. Công trình không có nội dung cho một sheet thì vẫn giữ sheet đó, đổi nội dung cho hợp (xem mục "Công trình mới hay cải tạo"). Bỏ sheet thì người dùng coi là bảng không dùng được.

## Thứ tự sheet và vai trò

| Sheet | Vai trò | Lấy số từ |
|---|---|---|
| `BOQ` | Bảng khối lượng có diễn giải từng dòng | `ThongSo`, `DienTich` |
| `MaDinhMuc` | Áp mã định mức cho từng công tác | `SoSanh` |
| `PhanKhu` | Bảng mã khu và sơ đồ lưới tô màu | nhập tay |
| `ThongSo` | Mọi thông số đầu vào, đặt theo mã | nhập tay |
| `DienTich` | Diện tích, chu vi phòng | nhập tay |
| `SoSanh` | Danh mục công tác theo khu, sheet trung tâm | `BOQ` |
| `CanXacNhan` | Điều đã chốt và điều cần hỏi | nhập tay |
| `VachKinh` | Phân tích đơn giá vách kính | `BOQ` |
| `CuaPN` (hoặc `CuaWC`, theo loại cửa) | Phân tích đơn giá 1 bộ cửa | `ThongSo`, `BOQ` |
| `TamTinh` | Định mức tự lập cho công tác không có mã | `BOQ` |

Chuỗi liên kết bắt buộc: `ThongSo` → `BOQ` → `SoSanh` (G = `BOQ!$H$n`, H = `BOQ!$C$n`) → `MaDinhMuc` (D, E lấy từ `SoSanh`; J = `SoSanh!G` × hệ số quy đổi I). Sửa một thông số ở `ThongSo` thì mọi sheet tự đổi.

## Định dạng chung

- Font Arial 11. Tiêu đề cột nền `D9E1F2`, chữ đậm. Dòng nhóm hạng mục nền `F2F2F2`.
- **Chữ xanh dương `0000FF`** = số nhập tay. **Chữ xanh lá `008000`** = liên kết sang sheet khác. **Nền vàng `FFFF00`** = giả định cần xác nhận. Ô công tác không có mã định mức tô `FCE4D6`.
- Định dạng số: kích thước `0.000`, khối lượng dòng con `0.00`, khối lượng hạng mục `#,##0.00`, tiền `#,##0`.

## Sheet BOQ

- Cột: STT | Hạng mục / diễn giải | ĐVT | Dài | Rộng | Cao/Dày | SL | Khối lượng | Ghi chú / vị trí DWG. Độ rộng gợi ý 6/58/7/10/9/10/7/13/48; cố định dòng tiêu đề (freeze `A5`).
- Nhóm A, B, C… ; mã hạng mục `A1`, `A1b`, `B3`… Dòng diễn giải bắt đầu bằng `"   - "`; dòng trừ dùng SL âm.
- Dòng diễn giải: `=IF(D="",1,D)*IF(E="",1,E)*IF(F="",1,F)*IF(G="",1,G)` (ô trống = 1). Dòng hạng mục: `=SUM(H các dòng con)`. Hạng mục đếm theo bộ thì nhập thẳng số vào H.
- Kích thước lấy từ thông số thì là công thức `=ThongSo!$C$n` (chữ xanh lá), không gõ số.
- Cột ghi chú luôn ghi **vị trí trên bản vẽ** (handle, tọa độ, tên block) để người khác kiểm lại.

## Sheet MaDinhMuc

- Cột: STT | Phân khu | Công tác | KL | ĐVT | Mã định mức đề xuất | Tên công tác theo định mức | ĐVT định mức | Hệ số quy đổi | KL theo ĐVT định mức | Điều chỉnh hao phí | Mã thay thế | Độ tin cậy | Ghi chú.
- Dòng nhóm theo khu (gộp ô B:N, tô màu khu), STT dạng `I.1`. Một công tác nhiều mã thì gộp ô A–E theo chiều dọc. Có freeze `D6` và bộ lọc.
- Hệ số quy đổi đổi đơn vị bóc sang đơn vị định mức: m² → 100 m² là `0.01`; cửa tính bộ mà định mức tính m khuôn thì I = `2 × cao + rộng`, tính m² cánh thì I = `rộng × cao`.
- Độ tin cậy: `chắc chắn` / `khá chắc` / `cần đối chiếu PDF` (tô vàng) / `tự lập` / `báo giá`. Ghi số trang PDF ở cột ghi chú.

## Sheet SoSanh

Cột: STT | Khu vực | (hiện trạng) | (cải tạo) | Công tác cần làm | Mã BOQ | Khối lượng | ĐVT | Mã khu. Gộp ô A–D theo khu. Mỗi dòng trỏ đúng một ô H của BOQ.

## Sheet ThongSo

Cột Mã | Thông số | Giá trị | Ghi chú/nguồn. Mã ngắn viết hoa (`HTANG`, `HDAM`, `HSAN`, `THEPCOT`…). Thông số suy ra từ thông số khác là công thức chữ đen. Ghi chú nêu **nguồn** (bản vẽ nào, cao độ nào) hoặc chữ "Giả định". Dòng cuối là chú thích màu.

## Ba sheet đơn giá (VachKinh, Cửa, TamTinh)

- Định mức lắp dựng thường **không có vật tư chính** (kính, khung, cửa). Các sheet này bóc thêm vật tư rồi cộng hao phí định mức: A. Vật liệu → B. Nhân công → C. Tổng → đơn giá bình quân = `IF(KL=0,0,Tổng/KL)`.
- Sheet cửa: khối thông số ở trên (phương án, rộng, cao, dài khuôn, diện tích cánh, các tham số tạm tính), bảng hao phí ở dưới, có dòng "số bộ theo BOQ" và thành tiền cả hạng mục.
- TamTinh: nhóm `TT-01`, `TT-02` tô `FCE4D6`; công tác con `TT-01a` tô `F2F2F2`, KL lấy từ BOQ; mỗi công tác có dòng Cộng và dòng Đơn giá; cột "Cách tính" nêu định mức được vận dụng.
- Cột đơn giá để trống, nền vàng, chờ nhập. Dòng cuối: "chưa tính chi phí chung, lợi nhuận, thuế".

## Công trình mới hay cải tạo

| Nội dung | Cải tạo | Xây mới |
|---|---|---|
| Mã định mức | Ưu tiên mã sửa chữa; mã xây mới thì nhân VL×1,02, NC×1,15, M×1,05 | Mã xây mới, cột điều chỉnh để "—" |
| SoSanh cột C, D | Hiện trạng ↔ Cải tạo | Bản vẽ thể hiện ↔ Quy cách thiết kế / giả định |
| Sheet cửa | Theo cửa chính của công trình | Đổi tên theo loại cửa nhiều nhất (ví dụ cửa WC) |

Liên quan: [[quy-trinh-boc-khoi-luong-tu-dwg]], [[ap-ma-tt38-cong-trinh-moi]].
