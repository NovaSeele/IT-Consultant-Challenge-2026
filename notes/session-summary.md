# Tóm tắt phiên làm việc với Claude (bàn giao sang chat local)

File này tóm tắt cuộc trao đổi trong phiên cloud "Tư vấn chuyên gia", để một chat mới trên máy có thể làm tiếp mà không cần đọc lại cả hội thoại.

## Bối cảnh

- Cuộc thi: IT Consultant Challenge 2026, Vòng 1 (Netcompany và Code MeLy). Đề: `IT Consultant Challenge 2026 - Round 1.pdf`. Ghi chú của BTC: `Info.txt`.
- Luật quan trọng: tối đa **10 slide tính cả bìa** (slide thứ 11 trở đi không được chấm), nộp **PDF**, ưu tiên tiếng Anh, **hạn 22h ngày 26/10/2026**.
- Bài nộp thẳng, **không có thuyết trình**: slide phải tự giải thích được.
- BTC không cho dùng AI tạo toàn bộ slide. Team phải tự viết lại câu chữ và hiểu mọi con số.
- Team Old Men: Nguyễn Việt Anh (Vanh), Vũ Văn Hậu, Nguyễn Hoàng Anh Dũng.

## Bài của team

- Vấn đề chọn: giao hàng và xử lý đơn (fulfilment).
- Giải pháp: một lớp kiểm soát chỉ đọc dữ liệu, đặt trên các hệ thống sẵn có. Mỗi nước có một adapter riêng; phần lõi dùng chung ghép mỗi đơn thành một timeline, phát hiện đơn sắp trễ, giao việc cho cửa hàng và báo sớm cho khách.
- MVP: Thụy Điển, 20 cửa hàng, 12 tuần. Sau đó Đan Mạch và Na Uy, rồi toàn bộ thị trường.
- Phân tích chi tiết: `solution-round-1.md`. Bản slide gốc 11 trang: `IT Consultant Challenge - Round 1 - Old Men.pptx/.pdf`.

## Góp ý đã đưa ra cho bản gốc

1. Thừa 1 slide, nên slide Business Impact sẽ không được chấm.
2. Lý do chọn fulfilment tự mâu thuẫn ("đề không nói rõ nên bỏ manual processes", trong khi chính bài cũng giả định rất nhiều).
3. Business case nhỏ, thiếu chi phí, con số 30% không có cách tính.
4. Slide 6 và slide 8 mâu thuẫn về "gợi ý cách xử lý".
5. Phần AI yếu ("AI viết tin nhắn" thì template cũng làm được).
6. Thiếu ai xử lý cảnh báo, thiếu team và go/no-go, thiếu lý do pilot ở Thụy Điển thay vì Đan Mạch.

## Bản v2 (đã làm)

- File: `IT Consultant Challenge - Round 1 - Old Men v2.pptx` và `.pdf`, đúng 10 slide. Bản gốc giữ nguyên.
- Script tạo lại slide: `tools/build_deck.py` (cần `pip install python-pptx`; font IBM Plex Sans và Georgia).
- Nội dung 10 slide:
  1. Bìa, kèm khung tóm tắt 4 dòng (vấn đề, giải pháp, MVP, lợi ích).
  2. Chuỗi nhân quả 4 vấn đề và ai bị ảnh hưởng.
  3. Bảng chấm điểm 4 vấn đề (fulfilment 12/12) và lợi ích cho từng nước.
  4. Giả định, có cột "kiểm chứng thế nào ở tuần 1–3".
  5. Kiến trúc giải pháp, kèm dải "vì sao không chọn phương án lớn hơn".
  6. Ví dụ đơn 1001 ("hôm nay thứ Hai"), so sánh có và không có hệ thống.
  7. AI: MVP chỉ có AI đọc email/PDF nhà cung cấp; Phase 2 có trợ lý ghép dữ liệu; Phase 3 có dự đoán trễ, gợi ý xử lý, trả lời khách. Khung "AI assists, rules decide".
  8. MVP: phạm vi, kế hoạch 12 tuần, đội 6 người, khoảng EUR 250k, điều kiện go/no-go.
  9. Triển khai 3 phase, vì sao Thụy Điển trước, ai xử lý cảnh báo, 4 rủi ro.
  10. Lợi ích: pilot khoảng EUR 135k/năm; toàn tập đoàn khoảng EUR 2M/năm; đầu tư khoảng EUR 750k; hoàn vốn trong khoảng 6 tháng sau khi triển khai hết.

### Các con số mới do Claude giả định (team cần rà và chốt)

- Đội thợ 4 người chờ 1 ngày mất khoảng EUR 1.500.
- 10% đơn giao lỗi; 60% số đó phát sinh trước khi xe chạy; sửa được một nửa khi phát hiện sớm 1 ngày, ra mức giảm 30% (1.200 đơn).
- EUR 100 mỗi đơn lỗi; EUR 40 mỗi giờ công; 5 phút mỗi cuộc gọi hỏi đơn.
- MVP khoảng EUR 250k; triển khai thêm khoảng EUR 500k; vận hành khoảng EUR 150k/năm.
- Khoảng 300 cửa hàng toàn tập đoàn (gấp 15 lần pilot).

## Góp ý của Vanh về slide 7 và cách đã xử lý

- "MVP (internal)" khó hiểu: đã bỏ, dùng chung các mốc MVP / Phase 2 / Phase 3 như slide 9; trợ lý ghép dữ liệu chuyển sang Phase 2.
- "The MVP works without AI": câu này đúng với bản gốc (MVP gần như không dùng AI), nhưng mâu thuẫn với v2 (MVP có AI đọc email nhà cung cấp) và dễ khiến giám khảo nghĩ AI chỉ để trang trí. Đã đổi thành "AI assists, rules decide": cảnh báo luôn đến từ quy tắc rõ ràng; AI chỉ đọc và gợi ý; chỗ nào AI không chắc thì chuyển người kiểm tra; AI hỏng thì nhập tay như hiện nay; AI không bịa ngày giao; model chạy tại EU theo GDPR.

## Việc còn lại của team

- [ ] Rà và chốt các con số giả định ở trên.
- [ ] Viết lại câu chữ theo cách của team.
- [ ] Cài font IBM Plex Sans, mở file v2, xuất PDF và kiểm tra lại.
- [ ] Nếu chữ nhiều quá, cắt bớt ở slide 4 hoặc slide 9.
