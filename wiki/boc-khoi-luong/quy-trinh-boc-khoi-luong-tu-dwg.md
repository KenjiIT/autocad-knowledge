---
title: Quy trình bóc khối lượng một tầng từ bản vẽ DWG
type: howto
topics: [boc-khoi-luong, cad, ket-cau, kien-truc]
status: confirmed
source: Phiên làm việc bóc khối lượng một tầng thương mại xây mới từ bộ DWG xuất từ Revit (mặt bằng, mặt đứng, mặt bằng dầm sàn), 11/2026
updated: 2026-11-05
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (05/11/2026)
---

# Quy trình bóc khối lượng một tầng từ bản vẽ DWG

Kết quả cuối là bảng theo [[bang-boc-khoi-luong-10-sheet]]. Trình tự dưới đây giúp mỗi con số có nguồn trên bản vẽ.

## 1. Gom đủ bản vẽ trước khi bóc

| Cần | Lấy từ |
|---|---|
| Cột, cửa, vách kính, thiết bị, tag phòng | Mặt bằng kiến trúc tầng |
| Chiều cao tầng, cao độ đỉnh kính, bệ, dầm mũ | Mặt đứng (đủ các hướng) |
| Dầm, sàn, chiều dày sàn, cao độ sàn | Mặt bằng dầm sàn kết cấu (có bảng thống kê dầm và ô chú thích hatch sàn) |
| Chiều cao dầm tầng trên (để trừ chiều cao cột) | Mặt bằng dầm sàn tầng trên |
| Thép | Bản vẽ bố trí thép. Không có thì tạm tính theo hàm lượng, tô vàng |

Bản vẽ "mặt bằng tải trọng" (loading map) không cho khối lượng; chỉ dùng để xác nhận cột chạy suốt, công năng ô sàn.

## 2. Đọc số liệu

- **Đọc cả file một lần thay vì từng đối tượng.** Đổi DWG sang DXF rồi đọc bằng ezdxf (xem [[do-dam-san-tu-mat-bang-ket-cau]] về cách đổi khi AutoCAD LT không xuất DXF). Đọc từng đối tượng qua MCP chỉ hợp với vài chục đối tượng.
- **Cột:** hatch SOLID trên `S-COLS` (khớp kích thước theo bbox) cộng cột vẽ tay bằng LINE trên `S-COLS` (thường trong khu WC). Cạnh khuất trong tường thì ghi giả định vào `ThongSo`.
- **Cửa, cửa sổ, thiết bị vệ sinh:** đếm block theo tên; tên block thường có kích thước (`1000x2200`). Ghi handle từng cái vào cột ghi chú.
- **Vách kính:** chiều dài theo tấm panel trên mặt bằng; chiều cao theo thanh nhôm trên mặt đứng. Tách ô sát nền và ô có bệ (thanh đứng bắt đầu từ cao độ bệ). Ô không thấy rõ trên mặt đứng thì suy ra từ ô bên cạnh và ghi "suy ra".
- **Diện tích phòng:** tag phòng có diện tích (không có kích thước). Vùng không có tag (thang bộ, sảnh thang máy, hành lang) thì tự đo theo mép tường và ghi tọa độ.
- **Chữ tiếng Việt vỡ thành nhiều MTEXT** (`\U+1EA6`…): ghép theo y rồi x trước khi đọc ghi chú.

## 3. Lập bảng

1. `ThongSo` trước: mọi chiều cao, chiều dày, hàm lượng thép, giả định. Mỗi dòng có nguồn.
2. `BOQ`: mỗi loại tiết diện / mỗi mặt đứng / mỗi tên dầm là một dòng diễn giải; kích thước lặp lại thì trỏ `ThongSo`.
3. `SoSanh` theo khu, `MaDinhMuc` áp mã (xem [[ap-ma-tt38-cong-trinh-moi]]).
4. Công tác không có mã → `TamTinh` (định mức tự lập, vận dụng mã gần nhất, nêu lý do).
5. `CanXacNhan`: liệt kê mọi giả định, chỗ bản vẽ mâu thuẫn, phần chưa bóc.

## 4. Kiểm tra trước khi giao

- Tính lại công thức (LibreOffice headless) đến khi **0 lỗi**.
- Đối chiếu tổng với số đã tính độc lập (tổng chiều dài, tổng bê tông, tổng số cửa).
- Vẽ lại kết quả đo (dầm, vùng sàn, phân khu) ra ảnh và soát bằng mắt với bản vẽ.
- Đối chiếu chéo giữa các bản: tiết diện cột trên mặt bằng kiến trúc và kết cấu; tiết diện dầm trong bảng thống kê và trên mặt bằng (xem [[loi-thuong-gap-boc-khoi-luong-qua-mcp]]).

## Quy ước tính thường dùng

- Cột: tiết diện × chiều cao tầng (trừ chiều dày sàn/dầm khi đã có); cốp pha = chu vi × chiều cao.
- Dầm: phần dưới sàn, b × (h − chiều dày sàn) × chiều dài thông thủy; cốp pha = [2 × (h − chiều dày sàn) + b] × chiều dài.
- Sàn: diện tích theo hatch trừ lỗ cột, lỗ thang; cốp pha sàn = diện tích sàn − đáy dầm.
- Thép tạm tính: khối bê tông × hàm lượng (kg/m³), tách thép đai và thép chủ theo tỷ lệ; luôn tô vàng.
