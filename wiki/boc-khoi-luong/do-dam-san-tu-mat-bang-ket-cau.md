---
title: Đo chiều dài dầm và diện tích sàn tự động từ mặt bằng dầm sàn
type: howto
topics: [boc-khoi-luong, ket-cau, dxf, ezdxf]
status: confirmed
source: Phiên làm việc bóc dầm, sàn một mặt bằng dầm sàn tầng trệt xuất từ Revit, khoảng 450 nét dầm, 11/2026. Bổ sung cho trang doc-mat-bang-ket-cau-revit
updated: 2026-11-05
reviewed_by: Claude Code, theo yêu cầu của Nguyen Khoi (05/11/2026)
---

# Đo chiều dài dầm và diện tích sàn tự động từ mặt bằng dầm sàn

Bổ sung cho [[doc-mat-bang-ket-cau-revit]] phần **đo khối lượng**.

## Đổi DWG sang DXF khi chỉ có AutoCAD LT

AutoCAD LT qua MCP không lưu được DXF. Dựng LibreDWG từ GitHub (cần cả submodule `jsmn`, nếu không sẽ lỗi thiếu `jsmn.h`). Các lệnh dưới viết cho môi trường Unix (Linux, WSL hoặc MSYS2); trên Windows thuần cần dựng bằng công cụ tương đương:

```
git clone --depth 1 https://github.com/LibreDWG/libredwg.git
git clone --depth 1 https://github.com/zserge/jsmn.git libredwg/jsmn
cd libredwg && mkdir build && cd build && cmake .. && make dwg2dxf
./dwg2dxf -y -o ban-ve.dxf ban-ve.dwg
```

Đọc DXF bằng ezdxf (lấy từ GitHub nếu không có pip). File gốc không bị sửa.

## Chiều dài dầm: ghép cặp nét cạnh

Dầm nằm dưới sàn vẽ bằng nét khuất trên `S-BEAM-HDLN`; dầm ở mép sàn chênh cote có một cạnh là nét mép sàn trên `A-FLOR`. Vì vậy:

1. Lấy LINE trên `S-BEAM-HDLN`, `S-BEAM`, `A-FLOR`, `A-FLOR-HDLN`.
2. Nhóm theo góc (làm tròn 0,5°), trong mỗi góc nhóm theo khoảng cách pháp tuyến (làm tròn 5 mm).
3. Hai nhóm song song cách nhau 190–850 mm là ứng viên một dầm. **Lấy phần giao** của hai cạnh (không lấy phần hợp): phần hợp làm dính nét mép sàn chạy dài, ra dầm giả.
4. Gán mỗi đoạn cho nhãn dầm gần nhất (nhãn `S-BEAM-IDEN` dạng `1F.HB1-400x600` và nhãn nhịp `HB1.2` trên `G-ANNO-TEXT`) cùng hướng, cách tim < 1,5 m. **Ưu tiên nhãn có bề rộng khớp** bề rộng đo được.
5. Bỏ đoạn có bề rộng lệch bảng thống kê quá 15 mm (30 mm với dầm xiên), bỏ ô giao dầm ngắn ≤ 600 mm, gộp đoạn trùng của cùng một dầm.
6. **Vẽ kết quả ra ảnh** (matplotlib, tô từng dầm, in tên) và soát với bản vẽ. Dầm thiếu thường do một cạnh nằm trên layer khác.

Đoạn đo được là chiều dài thông thủy (nét dầm bị cắt tại cột và dầm giao), dùng thẳng cho b × (h − chiều dày sàn) × L.

## Góc chữ MTEXT

Dùng `mtext.get_rotation()`. `mtext.dxf.rotation` trả 0 với chữ đứng vì hướng chữ lưu bằng vectơ; dùng nhầm sẽ gán nhãn dầm dọc cho dầm ngang.

## Diện tích sàn từ hatch

1. Khớp hatch trên mặt bằng với ô mẫu trong bảng chú thích theo **định nghĩa pattern** (góc, offset, dash), không theo tên (`FP_1`, `FP_6` là tên do bộ đổi đặt) hay màu.
2. Tính diện tích từng vòng biên bằng công thức shoelace trên `ezdxf.path.from_hatch(h)` đã làm phẳng. Vòng lớn có dấu dương là vùng sàn; các vòng nhỏ là lỗ (cột, lõi thang), lấy trị tuyệt đối để trừ. Một hatch có thể gồm nhiều vùng ngoài rời nhau.
3. Không dùng phép chẵn-lẻ bằng điểm giữa cạnh: điểm đó hay nằm trên cạnh chung của vòng khác, cho kết quả sai.
