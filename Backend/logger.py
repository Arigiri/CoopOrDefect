import os
from typing import List, Dict, Tuple
from datetime import datetime

class GameLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log_match(self, player1: str, player2: str, history: List[Dict[str, Tuple[str, int]]], winner: str):
        """Log match results to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.log_dir}/match_{player1}_vs_{player2}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Match: {player1} vs {player2}\n")
            f.write(f"Winner: {winner}\n")
            f.write("-" * 50 + "\n")
            
            if not history:
                f.write("\nTrận đấu kết thúc sớm do một bên timeout hoặc lỗi\n")
                return
                
            f.write("History:\n")
            for turn, state in enumerate(history):
                f.write(f"\nTurn {turn + 1}:\n")
                p1_decision, p1_score = state[player1]
                p2_decision, p2_score = state[player2]
                f.write(f"{player1}: {p1_decision} (Score: {p1_score})\n")
                f.write(f"{player2}: {p2_decision} (Score: {p2_score})\n")
            
            f.write("\n" + "-" * 50 + "\n")
            f.write(f"Final Scores:\n")
            # Lấy điểm cuối cùng từ history nếu có, nếu không thì ghi 0
            if history:
                f.write(f"{player1}: {history[-1][player1][1]}\n")
                f.write(f"{player2}: {history[-1][player2][1]}\n")
            else:
                f.write(f"{player1}: 0\n")
                f.write(f"{player2}: 0\n")
