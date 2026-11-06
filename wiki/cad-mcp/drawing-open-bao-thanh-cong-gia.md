---
title: drawing open báo "opened" nhưng bản vẽ không mở (AutoCAD đầy đủ)
type: pitfall
topics: [cad, mcp, autocad]
status: confirmed
source: Phiên thử mở file DWG qua MCP trên AutoCAD đầy đủ, 11/2026; đối chiếu với mã nguồn MCP. Bổ sung cho dòng "drawing open báo opened" trong trang loi-thuong-gap-boc-khoi-luong-qua-mcp
updated: 2026-11-06
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (06/11/2026)
---

# `drawing open` báo "opened" nhưng bản vẽ không mở (AutoCAD đầy đủ)

## Hiện tượng

Agent gọi `drawing` `operation=open` với đường dẫn đầy đủ. Tool trả thành công:

> opened: C:\...\ten-file.dwg

nhưng AutoCAD **không có tab mới**, và `drawing` `context` vẫn trả bản vẽ cũ. Đếm số bản vẽ đang mở bằng COM (`Documents.Count`) cũng không tăng.

Đây là hiện tượng **khác** với trường hợp bản vẽ đã mở sẵn trong phiên LT (xem [[loi-thuong-gap-boc-khoi-luong-qua-mcp]]): ở đó file có thật trong danh sách bản vẽ đang mở và chỉ cần `activate`.

## Nguyên nhân

Trên AutoCAD đầy đủ, mã gốc của MCP chạy lệnh `(command "_.OPEN" <đường dẫn>)` rồi **luôn trả "opened" mà không kiểm tra** file đã mở chưa. AutoCAD LT dùng một đường riêng (mở bằng `Documents.Open` và kiểm tra) nên không bị.

Từ launcher **0.2.13**, `drawing open` trên AutoCAD đầy đủ mở bằng COM (`Documents.Open`), kích hoạt bản vẽ và kiểm tra nó thật sự đang hoạt động. File đã mở sẵn thì chỉ kích hoạt (`already_open: true`); đường dẫn không tồn tại báo `E_PARAMETER_REJECTED`; không xác minh được thì báo `E_POSTCONDITION_MISMATCH` thay vì "opened".

## Cách kiểm tra bản vẽ thật sự đã mở

**Đừng tin chuỗi "opened".** Sau `open`, gọi `drawing` `context` và so `active_path` (hoặc `document_name`) với file đã yêu cầu. Chỉ khi khớp mới làm tiếp. Nên dùng `doc_id` và `lease_token` mới trong kết quả đó cho các lệnh sau.

## Khi gặp launcher cũ (trước 0.2.13)

- Cập nhật launcher.
- Trong lúc chờ: nhờ người dùng tự mở file, hoặc nếu file đã mở sẵn thì dùng `drawing` `activate` với `doc_id` của bản vẽ đó.

Nguyên tắc chung: sau mỗi thao tác làm đổi trạng thái, đọc lại trạng thái thật để xác minh, không dựa vào lời báo thành công của chính tool.
