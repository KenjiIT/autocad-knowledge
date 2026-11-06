---
title: Kênh COM bị khóa (poisoned) sau một lệnh đọc quá hạn
type: pitfall
topics: [cad, mcp, autocad, com]
status: confirmed
source: Phiên đọc một bản vẽ kết cấu lớn qua MCP, 11/2026; đối chiếu với mã nguồn MCP và nhật ký
updated: 2026-11-06
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (06/11/2026)
---

# Kênh COM bị khóa (poisoned) sau một lệnh đọc quá hạn

## Hiện tượng

Agent đọc cả một bản vẽ lớn trong một lệnh (ví dụ `drawing` `audit`), lệnh chạy lâu rồi báo:

> COM operation timed out and the STA worker was quarantined: drawing.audit

Từ đó **mọi lệnh sau đó đều bị từ chối**, dù AutoCAD vẫn chạy và phản hồi bình thường:

> COM STA worker is poisoned; refusing new work

Có thể kèm "acad.exe is alive but exposes no usable main window". Một lệnh khác (ví dụ chèn block) có thể đứng yên ở hàng đợi: trạng thái của gateway (`http://127.0.0.1:8764/status`) cho thấy `active_request` và `queued_requests` không giảm, trong khi nhật ký của MCP không có dòng mới. Chờ thêm không tự hết.

## Nguyên nhân

Mỗi lệnh COM có một hạn riêng (khoảng 30 đến 60 giây; launcher nới lên 600 giây cho `drawing.audit` và `entity.collect`). Lệnh nào **quá hạn** thì MCP coi luồng COM có thể đang treo, nên cách ly nó ("poisoned") và từ chối mọi việc mới cho tới khi dựng lại luồng. Bản vẽ không bị ảnh hưởng, chỉ kênh lệnh bị khóa.

Launcher từ bản 0.2.12 trở về trước có lỗi làm hạn đọc luôn là 60 giây (việc nới 600 giây không được áp dụng); bản 0.2.13 trở lên đã sửa. Hạn 600 giây cũng chỉ áp dụng cho hai thao tác trên, các thao tác đọc khác vẫn có hạn riêng.

## Cách xử lý

1. **Gọi `system` với `operation=init`.** Theo mã nguồn, lệnh này dựng lại backend (và luồng COM) mà không đóng bản vẽ hay tắt AutoCAD. Chưa kiểm chứng trên một kênh đang bị khóa thật.
2. Nếu vẫn bị khóa: **khởi động lại MCP** trong launcher (Thoát hẳn, mở lại, Bật kết nối cho agent) rồi mở phiên agent mới. Cách này đã khôi phục được kênh bị khóa. Bản vẽ đang mở không bị đụng tới.
3. Nhìn AutoCAD xem có **hộp thoại đang chờ bấm** không; hộp thoại treo là nguyên nhân thường gặp của lệnh chạy quá hạn.
4. Làm lại việc bị cắt, nhưng đọc theo cách ở mục dưới.

## Phòng tránh

- Với bản vẽ lớn, gọi `audit` một lần với `include_entities=false` để lấy tổng số và số lượng theo layer, rồi **chỉ đọc từng layer cần thiết**, tuần tự.
- Không gửi nhiều lệnh đọc nặng song song.
- Đọc cả bản vẽ bằng `entity.list` hoặc `entity.get` lặp lại cho hàng trăm đối tượng cũng chậm và dễ quá hạn: từ khoảng 100 đối tượng trở lên nên đổi sang DXF và đọc ngoại tuyến ([[do-dam-san-tu-mat-bang-ket-cau]]).
- Cập nhật launcher lên 0.2.13 trở lên.

Các lỗi khác khi dùng AutoCAD qua MCP: [[loi-thuong-gap-boc-khoi-luong-qua-mcp]].
