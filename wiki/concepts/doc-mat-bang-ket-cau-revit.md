# Đọc mặt bằng kết cấu DWG xuất từ Revit (kinh nghiệm)

Kinh nghiệm rút ra khi phân tích mặt bằng kết cấu tầng điển hình xuất từ Revit. Dùng cùng skill `autocad-identify-and-measure`.

1. **Đọc DXF bằng ezdxf trước, MCP sau.** Xuất DXF và đọc bằng môi trường Python có ezdxf và matplotlib (không có shapely). Cách này lấy đủ dữ liệu một lần và vẽ được ảnh từng vùng bằng `ezdxf.addons.drawing`. Khi vẽ, đặt `ax.set_aspect("auto")` và cho tỉ lệ figure bằng tỉ lệ vùng, nếu không giới hạn trục sẽ bị bỏ qua.
2. **Một DWG thường chứa nhiều view.** Gồm mặt bằng chính, mặt bằng "TOP LEVEL" và các mặt cắt đặt cạnh nhau trong Model. Tên view nằm ở đuôi tên block, ví dụ `...-3RD FLOOR FRAMING PLAN - TOP LEVEL`. Phải tách theo vùng X trước khi đếm.
3. **Đếm cột:** hatch SOLID trên `S-COLS`, không đếm cụm LINE. Ở công trình nhà ở, nhiều "cột" là vách ngắn trên `A-WALL-PATT`; báo riêng hai loại.
4. **Lỗ mở:** thường là ô vẽ dấu X bằng 2 đường chéo trên layer chi tiết (`A-DETL-CNTR`); mép lỗ là nét biên sàn. Phân biệt thang máy/thang bộ/hộp gen bằng block kiến trúc (`0 LIFT ...`, "lỗ gen kỹ thuật"). Kích thước chỉ dùng để suy luận.
5. **Độ dày sàn:** khớp hatch vùng sàn với ô mẫu trong bảng chú thích theo hình học pattern (số line, góc, tỉ lệ dash/offset). Hatch trên mặt bằng có thể là cùng pattern nhưng tỉ lệ khác với ô mẫu, và hai ô có thể cùng độ dày nhưng khác mẫu.
6. **Chữ tiếng Việt bị vỡ:** Revit xuất mỗi ký tự có dấu thành MTEXT riêng `\U+1ECA`. Phải ghép theo y rồi x để đọc ghi chú.
7. **Gối dầm:** kiểm tra đầu mút dầm (ghép cặp cạnh song song) so với bbox hatch cột/vách, dung sai bằng nửa bề rộng dầm + 60 mm. Kết quả chỉ là chỉ báo; cần xem ảnh để xác nhận.

## Quy tắc đề xuất dầm

- **Dầm bám cột/vách, không bám trục.** Dầm chính chạy giữa các cột, vách, cột dẹt hoặc cột khuất có thật. Dầm phụ chỉ gác lên dầm chính đã đứng trên cột/vách. Phép kiểm tra phải lần theo đường truyền tải: dầm nào đang đỡ dầm khác mà đầu mút không có cột/vách thì là lỗi.
- **Vách mỏng hơn dầm thì vẽ dầm liền qua.** Ví dụ cột dẹt 300 trên dầm 400: không cắt dầm tại mặt vách. Chỉ cắt dầm tại cột/vách dày bằng hoặc hơn bề rộng dầm, tại dầm khác hoặc tại lỗ mở. Sau khi gộp, kiểm lại chỗ chồng với dầm vuông góc.
- **Dầm đè lỗ mở:** trước khi sửa dầm hay lỗ, đối chiếu với bản vẽ nguồn xem lỗ có thật hay do đọc sai.

## Làm việc với AutoCAD LT qua MCP

- `cad_batch`: tham số mỗi bước phải nằm trong khoá `"params"` (`{"op":"create_text","params":{...}}`); đặt phẳng thì bị bỏ qua hoặc báo lỗi.
- `create_text` dùng căn giữa (J M), nên x, y là tâm chữ.
- Các lệnh `(command ...)` trên LT bị OSMODE của người dùng hút điểm. Nên tắt OSMODE tạm thời khi chạy lệnh nhận điểm và khôi phục ngay sau đó; lệnh đọc biến thì không cần bọc.
- Nếu người dùng chuyển sang bản vẽ khác trong lúc chạy, MCP có thể treo; chuyển lại rồi gọi `ensure_ready`.
- Khi có hai cửa sổ AutoCAD LT, MCP có thể báo "LT instance changed". Ghim đúng PID của phiên làm việc rồi gọi lại `ensure_ready`.
- Batch lớn có thể báo timeout dù đã chạy xong; đếm lại bằng `entity.count` trước khi chạy lại.

Bản vẽ **kiến trúc** đọc theo trang riêng [[doc-mat-bang-kien-truc-revit]]: căn hộ, phòng, nội thất, tiện ích, cây xanh. Đừng áp quy trình kết cấu (cột, dầm, sàn) lên bản kiến trúc.
