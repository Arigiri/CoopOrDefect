# Cooperate and Defect Game

Một game mô phỏng chiến lược hợp tác và phản bội, nơi các thuật toán AI đối đầu với nhau trong một giải đấu.

## Cấu trúc thư mục

```
MiniGame/
├── Algorithm/         # Thư mục chứa các thuật toán AI
├── Backend/          # Logic xử lý game
├── Frontend/         # Giao diện người dùng
├── CoopOrDefect/    # Thư mục chính của game
└── logs/            # Log kết quả các trận đấu
```

## Cách chơi

1. Mỗi trận đấu diễn ra giữa 2 AI
2. Mỗi lượt, mỗi AI sẽ chọn một trong hai quyết định:
   - C (Cooperate): Hợp tác
   - D (Defect): Phản bội

3. Điểm số được tính như sau:
   - Cả hai hợp tác (C-C): Mỗi bên được 3 điểm
   - Một bên hợp tác, một bên phản bội (C-D): 
     + Người hợp tác: 0 điểm
     + Người phản bội: 5 điểm
   - Cả hai phản bội (D-D): Mỗi bên được 1 điểm

4. Trận đấu kết thúc khi:
   - Một trong hai AI đạt >= 15 điểm
   - Nếu cả hai cùng đạt 15 điểm, người có điểm cao hơn thắng

## Cách thêm AI mới

1. Tạo file Python mới trong thư mục `Algorithm/`
2. Implement hàm `giveDecision(history)`:
   ```python
   def giveDecision(history):
       # history: List[Dict[str, Tuple[str, int]]]
       # Trả về 'C' hoặc 'D'
       return 'C'  # hoặc 'D'
   ```
   - `history`: Lịch sử các lượt đấu, mỗi lượt chứa quyết định và điểm của cả hai người chơi
   - Hàm phải trả về 'C' (hợp tác) hoặc 'D' (phản bội)

## Giao diện

1. Bên trái: Danh sách các trận đấu
   - Trận hiện tại được highlight màu xanh
   - Các trận đã đấu sẽ hiển thị kết quả

2. Giữa: Thông tin trận đấu
   - Tên hai AI đang đấu
   - Lịch sử các lượt đấu
   - Điểm số hiện tại

3. Bên phải: Bảng xếp hạng
   - Tên AI
   - Số trận thắng

4. Các nút điều khiển:
   - "Lượt tiếp": Chơi lượt tiếp theo trong trận hiện tại
   - "Trận tiếp": Chuyển sang trận tiếp theo (chỉ active khi trận hiện tại kết thúc)

## Yêu cầu hệ thống

- Python 3.6 trở lên
- Pygame 2.5.2

## Cài đặt và chạy

1. Clone repository này về máy:
```bash
git clone <repository_url>
cd MiniGame
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Chạy game:
```bash
python main.py
```

## Lưu ý

- Đảm bảo thư mục `logs` đã được tạo trước khi chạy game
- Các file AI trong thư mục `Algorithm` phải có hàm `giveDecision(history)` hợp lệ
- Game sẽ tự động tìm và load tất cả các file .py trong thư mục `Algorithm`
