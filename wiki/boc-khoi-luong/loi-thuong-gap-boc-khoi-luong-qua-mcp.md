---
title: Lỗi thường gặp khi bóc khối lượng qua AutoCAD LT và MCP
type: pitfall
topics: [cad, mcp, boc-khoi-luong]
status: confirmed
source: Phiên làm việc bóc khối lượng nhiều bản vẽ mở cùng lúc trên AutoCAD LT qua MCP, 11/2026
updated: 2026-11-05
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (05/11/2026)
---

# Lỗi thường gặp khi bóc khối lượng qua AutoCAD LT và MCP

| Hiện tượng | Nguyên nhân | Cách làm |
|---|---|---|
| `cad_batch` `get` chỉ trả handle | Thiếu `verbose: true` | Đặt `verbose: true`; tham số nằm trong `params` (`{"op":"get","params":{"entity_id":"1A2"}}`) |
| Đọc vài trăm đối tượng qua `cad_batch` rất chậm và tốn ngữ cảnh | Mỗi đối tượng trả vài trăm ký tự | Từ khoảng 100 đối tượng trở lên: đổi DWG sang DXF và đọc offline ([[do-dam-san-tu-mat-bang-ket-cau]]) |
| `drawing activate` báo `E_DOCUMENT_ID_MISMATCH` / `E_DOCUMENT_LEASE_MISMATCH` | Truyền đường dẫn, hoặc lease của bản đang mở | Truyền `doc_id` **và** `lease_token` của chính bản vẽ đích. Lấy cả hai từ lỗi trả về khi gọi với `doc_id` đúng |
| `drawing open` báo "opened" nhưng tab không đổi | Bản vẽ đã mở sẵn trong phiên LT | Dùng `activate` với `doc_id`, hoặc nhờ người dùng bấm tab |
| Không zoom / chụp được mặt đứng | Bản vẽ đang ở Layout (paper space) | Đọc thẳng dữ liệu đối tượng thay vì chụp |
| File DWG nằm ngoài thư mục được cấp | Quyền thư mục theo từng phiên | Xin quyền đúng thư mục chứa bản vẽ trước khi chuyển file |
| Nhãn dầm dọc gán nhầm cho dầm ngang | `mtext.dxf.rotation` = 0 với chữ đứng | Dùng `mtext.get_rotation()` |
| Bảng thống kê dầm và mặt bằng ghi khác tiết diện (ví dụ 500x600 và 400x600) | Lỗi hồ sơ | Tính theo nét vẽ và nhãn trên mặt bằng, ghi mâu thuẫn vào `CanXacNhan` |
| Ô ghi chú trong Excel hiện `#N/A` / `#NAME?` | Chữ bắt đầu bằng `=` bị hiểu là công thức | Không mở đầu ghi chú bằng `=`; viết "Công thức: …" |
| Không cài được `pymupdf` / `ezdxf` bằng pip | Môi trường không ra được PyPI | Dùng `pdftotext -layout` cho PDF; lấy ezdxf từ GitHub và đặt `PYTHONPATH` |

Các lỗi khác của AutoCAD LT qua MCP (hai cửa sổ LT, OSNAP hút điểm, đường dẫn có dấu) nằm ở mục "Làm việc với AutoCAD LT qua MCP" của [[doc-mat-bang-ket-cau-revit]].
