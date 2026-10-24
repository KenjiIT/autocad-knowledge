# Đọc mặt bằng kiến trúc DWG xuất từ Revit (kinh nghiệm)

Kinh nghiệm rút ra khi phân tích mặt bằng kiến trúc căn hộ xuất từ Revit. Bản kiến trúc trả lời các câu hỏi khác bản kết cấu: có bao nhiêu căn, mỗi căn mấy phòng, nội thất gì, có những khu chức năng nào, bố trí ra sao, đo đạc thế nào, cây xanh ở đâu. Không đếm cột/dầm như bản kết cấu ([[doc-mat-bang-ket-cau-revit]]); chỉ đối chiếu với kết cấu khi người dùng hỏi.

1. **Nhận biết loại bản vẽ** qua mã số và layer. A-xxx là kiến trúc, S-xxx là kết cấu. Bản kiến trúc có `A-FLOR-FURN`, `P-FIXT`, `A-TAGS-ROOM`, `A-FLOR-DOOR`, `A-FLOR-WNDW`. Bản kết cấu có `S-BEAM`, `S-COLS`, bảng độ dày sàn.
2. **Nhiều view trong một Model:** mỗi tầng hoặc nhóm tầng là một view, nhận ra qua đuôi tên block (ví dụ `... - Tầng 3`, `... - Tầng 4-7`). Tách theo vùng X. Bảng cao độ tầng có thể đặt rất xa view.
3. **Layer hậu tố `-1`** là model liên kết (căn hộ). Không hậu tố là model công trình (lõi, hành lang, tiện ích).
4. **Tên family Revit cho biết loại và kích thước**, ví dụ:
   - `0 SWA - 1 FLUSH - 800x2400_INT` (cửa phòng ngủ)
   - `IntAys … Double Entrance door` (cửa chính căn hộ)
   - `0 LIFT - SERVICE LIFT`
   - `double_bed_king`, `PMH_diningx6`
   - `Planting 1-2` (cây lớn), `Planting 3 array` (hàng rào cây)

   Đếm theo tên family sau khi bỏ đuôi tên view.
5. **Số căn = số cửa chính căn hộ.** Đối chiếu thêm với nhãn "CĂN HỘ n / x-PHÒNG NGỦ / (LL) xxx m²" đặt ngoài đường bao. LL là diện tích lọt lòng; dùng số này, không dùng diện tích raster.
6. **Tách phòng/căn tự động:**
   - Raster 50 mm/px các layer tường, cột, kính, cửa sổ, lan can.
   - Vẽ bbox block cửa thành khối đặc để đóng ô cửa.
   - `PIL.ImageDraw.floodfill` từng vùng trống, mỗi vùng là một phòng.
   - Gán nội thất vào phòng theo tâm bbox, rồi gọi tên phòng: giường → phòng ngủ; bồn cầu/sen/bồn tắm → WC; bếp nấu/tủ lạnh → bếp; sofa/bàn ăn → khách/ăn; cục nóng điều hòa → lô gia kỹ thuật.
   - Hợp các phòng nối nhau qua cửa nội bộ thành một căn; bỏ cửa chính, cửa thoát hiểm, cửa thang máy.
   - Phòng có cửa không chạm vùng sẽ bị tách lẻ, cần soát lại.
7. **Khu ngoài căn hộ:** đọc `A-TAGS-ROOM` (tên + diện tích), `G-TEXT` (SWIMMING POOL, CANOPY…) và nội thất đặc trưng: ghế tắm nắng → sàn hồ bơi, dãy tủ + lavabo → phòng thay đồ, quầy + ghế đôn → pantry, thùng rác → phòng rác, `Raiser` → hộp kỹ thuật.
8. **Cách ghi kích thước:** thường chỉ có chuỗi kích thước lưới trục (trên + hai bên, kèm dim tổng). Cao độ dùng ký hiệu `FFL`; mặt cắt được tham chiếu bằng mã bản vẽ mặt cắt. Kích thước phòng thường chỉ có ở dạng diện tích.
9. **Chữ tiếng Việt bị vỡ:** ghép MTEXT theo hướng chữ (kể cả chữ xoay 90°), thay `\U+XXXX` bằng ký tự thật.
