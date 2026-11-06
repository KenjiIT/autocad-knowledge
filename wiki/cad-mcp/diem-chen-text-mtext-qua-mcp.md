---
title: Điểm chèn của TEXT và MTEXT khi tạo qua MCP
type: pitfall
topics: [cad, mcp, autocad, chu]
status: confirmed
source: Phiên vẽ chi tiết và bảng thống kê vào bản vẽ có sẵn qua MCP, 11/2026; phải dời chữ sau khi tạo
updated: 2026-11-06
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (06/11/2026)
---

# Điểm chèn của TEXT và MTEXT khi tạo qua MCP

## Hiện tượng

Agent tính tọa độ tâm để căn giữa chữ trong ô bảng, dưới ký hiệu mặt cắt hay trong vòng tròn số hiệu, nhưng chữ lệch sang phải và lên trên.

## Nguyên nhân

Tool tạo chữ không có tham số căn lề:

| Loại | Điểm chèn `(x, y)` là |
|---|---|
| TEXT (`type: text`, `annotation create_text`) | góc **dưới-trái** dòng chữ |
| MTEXT (`type: mtext`, `entity create_mtext`) | góc **trên-trái** khối chữ (`attachment_point` = 1) |

## Cách làm

- Căn giữa TEXT: `x = x_tâm − n × 0,9 × h / 2`, `y = y_tâm − h / 2` (n là số ký tự, h là chiều cao chữ; hệ số 0,9 là ước lượng, đọc lại `bounds` để chỉnh).
- Ô bảng với MTEXT: `x = mép trái ô + lề`, `y = mép trên ô − (chiều cao ô − h) / 2`.
- Chữ đã lệch: dùng `entity move` với `data: {dx, dy}` tính từ `bounds` trả về.

## Kiểm tra

So `bounds` của chữ với khung ô hoặc ký hiệu: chữ phải nằm trọn bên trong, không chạm nét.
