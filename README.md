# autocad-knowledge

Tri thức đọc và làm việc với bản vẽ AutoCAD (DWG xuất từ Revit) dùng cùng [AutoCAD MCP Launcher](https://github.com/KenjiIT/autocad-mcp-launcher). Các trang nằm trong `wiki/`; bắt đầu từ [`wiki/index.md`](wiki/index.md).

Đây là bản công khai, đã bỏ tên và số liệu của dự án cụ thể. Nội dung là kinh nghiệm tham khảo; hãy kiểm tra lại trên bản vẽ của bạn trước khi dựa vào.

## Cách lấy tri thức

- **Qua launcher (khuyến nghị):** launcher tải **bản phát hành mới nhất** (tag `vX.Y.Z`) về `~/autocad-knowledge`, kiểm tra SHA-256, và kiểm tra bản mới mỗi 24 giờ. Agent đọc bằng tool `knowledge`.
- **Thủ công:** tải `autocad-knowledge-wiki.zip` ở trang [Releases](../../releases), hoặc `git clone`.

Nhánh `main` có thể chứa thay đổi chưa đóng tag. Launcher chỉ nhận các bản đã đóng tag, tức là đã qua người duyệt.

## Dành cho người duyệt: phát hành một bản

1. Đưa các trang đã duyệt vào `wiki/<nhóm>/`, thêm một dòng vào `wiki/index.md`, rồi push lên `main`.
2. Chạy kiểm tra: `python tools/lint.py --root .` (lỗi nhạy cảm phải sạch; dùng `sensitive-terms.local.txt` chứa mã dự án đang làm, **không** đưa file này lên git).
3. **Chỉ đẩy tag**, workflow tự kiểm tra, dựng gói và tạo Release (đừng tạo Release thủ công: thiếu tệp đính kèm thì launcher không cập nhật được):

   ```
   git tag v0.2.0
   git push origin v0.2.0
   ```

   Số phiên bản: tăng số giữa (`0.x.0`) khi thêm hoặc sửa trang đáng kể, số cuối (`0.0.x`) khi sửa lỗi chính tả hoặc chú thích nhỏ.
4. Nên đặt bí mật `SENSITIVE_TERMS` của repo (Settings, Secrets and variables, Actions): các mã dự án và tên khách hàng, ngăn cách bằng dấu phẩy, để bước kiểm tra trong workflow chặn được chúng.

Trang đã duyệt là dữ liệu tham khảo công khai, không phải lệnh cho agent.
