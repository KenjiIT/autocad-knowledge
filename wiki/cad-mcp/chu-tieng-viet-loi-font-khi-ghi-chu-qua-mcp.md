---
title: Chữ tiếng Việt bị lỗi font khi ghi chú qua MCP
type: pitfall
topics: [cad, mcp, autocad, chu, font]
status: confirmed
source: Phiên vẽ chi tiết kết cấu vào một bản vẽ có sẵn trên AutoCAD bản đầy đủ qua MCP, 11/2026; người dùng phát hiện lỗi hiển thị
updated: 2026-11-06
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (06/11/2026)
---

# Chữ tiếng Việt bị lỗi font khi ghi chú qua MCP

## Hiện tượng

Chữ tạo bằng `entity create_batch` (`type: text`), `annotation create_text` hoặc `entity create_mtext` hiện sai dấu tiếng Việt trên màn hình AutoCAD. Kết quả trả về vẫn đúng chuỗi Unicode (`actual.text` khớp `requested.text`), nên agent tưởng đã xong.

## Nguyên nhân

Đối tượng chữ mới nhận kiểu chữ **hiện hành** của bản vẽ, thường là `Standard` dùng font SHX `txt`. Font này không có ký tự tiếng Việt. Tool tạo chữ không có tham số chọn kiểu chữ. `drawing set_variables` cũng không đặt được `TEXTSTYLE` (trả `E_VARIABLE_REJECTED`, biến không nằm trong danh sách cho phép).

## Cách làm

1. **Trước khi ghi chữ**, đọc bảng kiểu chữ của bản vẽ và xem chữ có sẵn dùng kiểu nào. Có bản DXF thì đọc bảng `STYLE` (mã 2 = tên kiểu, mã 3 = tệp font) và mã 7 của các TEXT/MTEXT cùng layer. Chọn kiểu chữ dùng font TrueType có tiếng Việt mà bản vẽ đang dùng cho ghi chú.
2. Tạo chữ bằng **MTEXT** và ghi font ngay trong nội dung:
   `{\fTên họ font|b0|i0|c0|p0;Nội dung tiếng Việt}`
   Tên họ font là tên hiển thị của font TrueType (ví dụ `Arial`), không phải tên tệp `.ttf`. Trong DXF, tên này nằm ở dữ liệu mở rộng 1000 của kiểu chữ tương ứng.
3. MTEXT bắt buộc `width` > 0 (trả `mtext width must be positive` nếu bằng 0). Đặt `width` rộng hơn chuỗi (khoảng số ký tự × chiều cao × 0,95 + 2 × chiều cao) để chữ không tự xuống dòng.
4. Chữ đã tạo sai font: tạo lại bằng MTEXT ở cùng vị trí rồi xóa bản cũ. Không có tool đổi kiểu chữ của đối tượng có sẵn.

## Kiểm tra

- Đọc lại `bounds`: chiều cao khối chữ lớn hơn khoảng 1,8 lần chiều cao chữ nghĩa là chữ đã xuống dòng.
- Nhờ người dùng nhìn tab AutoCAD (hoặc chụp màn hình nếu thư mục ảnh được cấp quyền). Kết quả trả về của tool không chứng minh chữ hiển thị đúng.
- Máy không có font đã chọn thì AutoCAD thay font khác; khi nghi ngờ, dùng `Arial`.

Vị trí điểm chèn của TEXT và MTEXT: [[diem-chen-text-mtext-qua-mcp]].
