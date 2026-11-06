---
title: cad_batch kẹt "Only one AutoCAD transaction may be active" sau lỗi giữa chừng
type: pitfall
topics: [cad, mcp, autocad, batch]
status: confirmed
source: Phiên vẽ chi tiết kết cấu khoảng 300 đối tượng qua MCP trên AutoCAD bản đầy đủ, 11/2026
updated: 2026-11-06
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (06/11/2026)
---

# cad_batch kẹt "Only one AutoCAD transaction may be active" sau lỗi giữa chừng

## Hiện tượng

1. Một `cad_batch` nhiều lệnh tạo đối tượng lỗi giữa chừng (ví dụ `E_AUTOCAD_INSTANCE_UNVERIFIED`). Phần đã tạo trước lỗi **vẫn nằm trong bản vẽ**, không được hoàn tác dù mô tả nói lô lệnh sẽ hoàn tác khi lỗi.
2. Từ đó mọi `cad_batch` đều báo `E_TRANSACTION_BEGIN`: "Only one AutoCAD transaction may be active at a time".
3. `system recover` không gỡ được. `transaction commit` cần mã giao dịch mà agent không có.

## Cách làm

- **Đếm lại phần đã tạo** (`entity count` theo layer, hoặc `get` các handle trả về) trước khi gửi lại, để không vẽ trùng.
- Tạo tiếp bằng **`entity` `create_batch`** với `data.entities` (mỗi mục có `type`: `line`, `circle`, `polyline`, `text`, `mtext` kèm tọa độ và `layer`). Lệnh này chạy trọn gói, tự commit và vẫn dùng được khi `cad_batch` đang kẹt. Đã chạy được lô hơn 100 đối tượng.
- Xóa, dời: gọi `entity erase` hoặc `entity move` từng đối tượng, truyền `expected_revision` tăng dần 1 sau mỗi lệnh.
- Chưa thử: `system` `operation=init` hoặc khởi động lại MCP trong launcher (cách đã gỡ được lỗi kênh COM bị khóa, xem [[khoa-kenh-com-poisoned]]).

## Phòng tránh

- Ưu tiên `entity create_batch` cho việc tạo nhiều đối tượng, dùng `cad_batch` khi cần trộn tạo, sửa, đọc.
- Chia lô vừa phải, kiểm tra kết quả từng lô trước khi gửi lô sau.
