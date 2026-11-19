# Vỏ để bàn ES3C28P (ESP32-S3 + LCD 2.8")

Vỏ dạng nêm, màn hình nằm ngang và ngả ra sau 18°. Mô hình dựng bằng **SolidCraft** và có 2 phiên bản:

| | Tiêu chuẩn | XL |
|---|---|---|
| Kích thước ngoài (rộng × sâu × cao) | 90.8 × 65 × 57.2 mm | 102.8 × 86 × 57.2 mm |
| Khoang pin tối đa (dài × rộng × dày) | 67.5 × 36 × 8 mm | 84 × 50.5 × 8.5 mm |
| Pin phù hợp | 503450, 603450, 803450, 603460, 803460 | 805080 (~3000 mAh) |
| Vít (lục giác chìm) | 4 × M3×12 | 4 × M3×12 + 2 × M3×6 |
| Ốc cấy nhiệt M3 (heat-set insert, dài ≤ 4 mm, Ø ngoài 4.2–4.6 mm) | 4 | 6 |
| Công tắc gạt mini SS12D00G3 (cần gạt 3 mm) | 1 | 1 |
| Thư mục file in | `solidcraft/print/` | `solidcraft/print_xl/` |
| File thiết kế | `es3c28p_case.sc` | `es3c28p_case_xl.sc` |

Xem mô hình 3D: mở `es3c28p_viewer.html` bằng trình duyệt (xoay, tách lớp, mặt cắt, chuyển giữa 2 bản).

Ở mỗi thư mục file in có:
- `front_bezel.stl` và `rear_body.stl`: đã đặt sẵn đúng hướng in.
- File `.3mf` chứa cả 2 chi tiết, mở thẳng trong slicer.
- File `.step` của từng chi tiết.

## Công tắc ngắt pin
Công tắc **SS12D00G3** gắn ở thành bên trái, **ngang bằng cổng USB‑C** và nằm phía sau cổng. Khe cần gạt song song với lỗ USB, nên cần gạt trượt lên–xuống.
- **Khung giữ:** bên trong thành có một khung ôm thân công tắc, kích thước 9.0 × 4.0 mm.
  - Đặt công tắc vào sao cho cần gạt lọt qua khe 4.5 × 2.2 mm, rồi nhỏ một giọt keo nến hoặc keo dán vào mép khung để cố định.
  - Thành vỏ ở chỗ này mỏng 1.2 mm, nên cần gạt 3 mm nhô ra ngoài khoảng 1.8 mm.
- **Đấu dây:** cắt **dây đỏ (+)** của pin, nối vào chân giữa và một chân bên của công tắc, hàn rồi bọc co nhiệt. Dây đen giữ nguyên.
- **Lưu ý:**
  - Công tắc chỉ ngắt pin. Khi cắm USB‑C, bo vẫn chạy bằng điện USB.
  - Khi công tắc tắt thì pin cũng **không được sạc**. Muốn sạc, bật công tắc rồi cắm USB.
- Có thể dùng bản G4 (cần gạt 4 mm) nếu muốn cần gạt nhô ra nhiều hơn.

## Lắp ráp
Vít không vặn thẳng vào nhựa. Mỗi vấu của mặt trước có một **lỗ Ø4.0 sâu 4.5 mm để cấy ốc nhiệt M3** (heat-set insert), miệng lỗ quay về phía bo mạch.
- Lỗ cố ý nhỏ hơn Ø ngoài của insert (4.2–4.6 mm) để nhựa chảy ôm chặt insert.
- Cách cấy: úp mặt trước xuống bàn, đặt insert lên miệng lỗ. Dùng mỏ hàn khoảng 220 °C (PLA) hoặc 245 °C (PETG) ấn thẳng xuống từ từ, đến khi mặt insert bằng hoặc thấp hơn mặt vấu khoảng 0.2 mm, rồi nhấc mỏ hàn ra.
- Insert dài tối đa 4 mm. Nếu insert của bạn có Ø ngoài khác, sửa `INSERT_D` trong `make_script.py`, thường là Ø ngoài trừ đi 0.3–0.5 mm.

**Bản tiêu chuẩn**
1. Cấy **4 ốc cấy nhiệt M3** vào 4 vấu của mặt trước.
2. Dán pin vào khoang, cắm dây pin vào bo.
3. Đặt bo vào mặt trước, mặt kính úp vào cửa sổ.
4. Úp thân sau lên.
5. Bắt 4 vít M3×12 từ phía sau (2 vít trên lưng, 2 vít dưới đáy). Mỗi vít đi xuyên cột của thân sau và PCB rồi vặn vào insert.

**Bản XL** (pin 805080 nằm chắn đường đi của 2 cột vít dưới, nên đổi cách bắt vít)
1. Cấy **6 ốc cấy nhiệt M3** vào mặt trước: 4 vấu ở lỗ PCB và 2 vấu hai bên mép bo.
2. Đặt bo vào mặt trước. Bắt **2 vít M3×6** qua 2 lỗ dưới của PCB, vặn từ mặt sau bo vào insert.
3. Dán pin vào khoang, cắm dây pin vào bo.
4. Úp thân sau lên.
5. Bắt **4 vít M3×12** vào insert:
   - 2 vít trên lưng: đi qua 2 lỗ trên của PCB.
   - 2 vít dưới đáy, ở hai bên: vào 2 vấu nằm ngoài mép bo.

Khớp nối giữa mặt trước và thân sau là **khớp bậc**: phần trong của thành mặt trước kéo dài xuống 2.5 mm và lọt vào bậc khoét trên thân sau.

## Chỉnh trong SolidCraft
Mở file `.sc` rồi vào **Change Parameters**. Các tham số chính được đánh dấu yêu thích:

| Tham số | Mặc định | Khoảng an toàn |
|---|---|---|
| `TH` (góc ngả) | 18° | 15–21° |
| `WALL` (độ dày thành) | 2 mm | 1.6–2.4 mm |
| `FIL` (bo tròn cạnh ngoài) | 3 mm | 2.6–4 mm |
| `LB` (chiều dài đế) | 65 mm (XL: 86 mm) | 62–70 mm (XL: 82–90 mm) |
| `ZTB` (độ dày phần trên-sau) | −12 mm | −10 đến −15 mm |

Với cả hai bản, mình đã thử đổi từng tham số tới hai đầu khoảng rồi đưa về mặc định. Mô hình dựng lại không có lỗi, không có cảnh báo, và luôn ra đúng một khối liền.

Muốn đổi lớn hơn khoảng trên (ví dụ cỡ pin khác), sửa số ở đầu `solidcraft/make_script.py` rồi dựng lại:
```
python make_script.py standard
python make_script.py xl
solidcraft-cli run es3c28p_case_xl_script.json --save es3c28p_case_xl.sc
```

## Lỗ mở (cả 2 bản)
- **USB-C**: ở cạnh trái, lỗ 12.8 × 7.2 mm.
  - Bản XL có thêm một **hốc lõm 24 × 12 mm** quanh cổng. Thành ở đáy hốc chỉ dày 2 mm và nằm sát cổng, nên không còn đường hầm sâu. Nóc hốc vát 45°, in vẫn không cần support.
- **Không mở khe thẻ microSD.** Muốn cắm hoặc rút thẻ thì tháo 4 vít để mở vỏ.
- **6 khe thoát nhiệt** ở mặt sau.

## In (không cần support)
In bằng PLA hoặc PETG, lớp 0.2 mm, 3 vách. Trong slicer, **tắt support**.
Dùng file STL trong `print/` hoặc `print_xl/`, vì các file này đã xoay sẵn đúng hướng in. Đừng dùng file `*_assembly.step`: file đó nằm theo hướng lắp ráp nên in sẽ phải có support.

- **Thân sau**: úp **miệng xuống bàn in**.
  - Các mặt dốc nhất nghiêng 43° (bản tiêu chuẩn) và 28° (bản XL) so với phương thẳng đứng.
  - Cột vít đứng thẳng.
  - Gân giữ pin đã vát dốc ≤ 41°.
  - Những chỗ còn lại mà slicer có thể tô đỏ đều tự in được:
    - Gờ bậc 1 mm quanh miệng.
    - Đỉnh khoang bo tròn rộng 1.4 mm.
    - Nóc lỗ USB-C: rất nhỏ, tự in được.
  - 6 khe thoát nhiệt được khoét nghiêng 45° so với phương thẳng đứng khi in. Nóc khe vừa đúng 45° nên không cần support, và mép khe không bị mỏng nhọn.
- **Mặt trước**: úp **mặt kính xuống bàn in**.
  - Chỉ có chân góc bo tròn R3 sát bàn in và vát 45° của cửa sổ.
  - Cả hai đều in tốt mà không cần support.
- **Không nên** in thân sau đặt đáy xuống bàn. Khi đó các cột vít nằm gần như ngang nên bắt buộc phải có support.

Gắn thêm 4 chân cao su Ø10 × 1 mm vào đáy (không bắt buộc).

## Đã kiểm tra
- **Va chạm**: dùng lệnh Interference của SolidCraft, chèn file STEP gốc của bo cùng một khối pin giả đúng kích thước tối đa. Ở cả 2 bản đều không có va chạm.
  - Riêng cặp mặt trước với tấm kính cảm ứng thì SolidCraft không tính được. Theo thiết kế, ở đó có khe hở 0.2 mm.
- **Liền khối**: mỗi chi tiết là đúng một khối liền, lưới STL kín.
- **Độ dày thành**: đã đo trên toàn bộ STL bằng `solidcraft/check/wall_thickness.py`. Không còn thành nào mỏng hơn 0.8 mm. Chỗ mỏng duy nhất còn lại là các cạnh vát sắc ở miệng lỗ vít xiên và ở đỉnh gân, không phải thành.
- **Sketch**: mọi sketch đều đủ ràng buộc (dof 0).

## Cấu trúc thư mục
| Đường dẫn | Nội dung |
|---|---|
| `solidcraft/make_script.py` | Bộ sinh script lệnh SolidCraft cho cả 2 bản (`python make_script.py standard` hoặc `xl`) |
| `solidcraft/es3c28p_case*_script.json` | Script lệnh đã sinh, dựng lại từ đầu bằng `solidcraft-cli run` |
| `solidcraft/es3c28p_case*.sc` | File thiết kế SolidCraft, có lịch sử và tham số |
| `solidcraft/es3c28p_case*_assembly.step` | Bản lắp ráp, cùng hệ toạ độ với file STEP của bo |
| `solidcraft/print/`, `solidcraft/print_xl/` | File in STL, 3MF, STEP đã xoay đúng hướng |
| `solidcraft/check/` | Script kiểm tra và ảnh chụp |
| `comps.json` | Khung bao các linh kiện, trích từ file STEP của bo. `make_script.py` dùng file này để tránh linh kiện |

## Dựng lại và kiểm tra
Chạy trong thư mục `solidcraft/`:
```
python make_script.py standard
solidcraft-cli run es3c28p_case_script.json --save es3c28p_case.sc
solidcraft-cli run check/export_print.json --in es3c28p_case.sc
solidcraft-cli run check/walk.json --in es3c28p_case.sc
python check/wall_thickness.py print/rear_body.stl 0.8
```
- Với bản XL thì dùng `xl`, `es3c28p_case_xl*` và `walk_xl.json` / `export_print_xl.json`.
- `check/walk.json`: đổi từng tham số tới hai đầu khoảng an toàn để kiểm tra mô hình dựng lại không lỗi.
- `check/wall_thickness.py`: đo độ dày thành trên file STL. Cần thư viện `trimesh`.
- `check/fit_*.json`: kiểm tra va chạm với bo mạch, pin giả và công tắc giả. Cần file STEP của bo **ES3C28P_3D.step** (tải từ lcdwiki.com) đặt vào `solidcraft/check/`. File này của nhà sản xuất nên không đưa vào repo.

## Chưa làm
- Chưa in thử thực tế.
- Nút BOOT/RESET nằm bên trong vỏ.
- Vỏ không chừa chỗ cắm dây cho 2 cổng MX1.25 4P ở cạnh dưới của bo.
