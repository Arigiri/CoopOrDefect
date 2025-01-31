import os
import sys
from Frontend.main import Game

if __name__ == "__main__":
    # Đảm bảo thư mục hiện tại là thư mục gốc của project
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Khởi chạy game
    game = Game()
    game.run()
