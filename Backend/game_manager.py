import os
import importlib.util
import signal
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

Decision = str  # 'C' or 'D'

@dataclass
class Player:
    name: str
    module: object
    total_score: int = 0
    matches_won: int = 0  # Số trận thắng

@dataclass
class Match:
    player1: Player
    player2: Player
    history: List[Dict[str, Tuple[Decision, int]]]
    winner: Optional[str] = None
    
    def is_finished(self) -> bool:
        """Trận đấu kết thúc khi một trong hai người chơi đạt >= 15 điểm"""
        return (self.player1.total_score >= 15 or 
                self.player2.total_score >= 15)
    
    def get_winner(self) -> Optional[str]:
        """Xác định người chiến thắng dựa trên điểm số"""
        if not self.is_finished():
            return None
        
        if self.player1.total_score >= 15 and self.player2.total_score >= 15:
            # Nếu cả hai cùng đạt 15 điểm trong lượt cuối, người có điểm cao hơn thắng
            if self.player1.total_score > self.player2.total_score:
                return self.player1.name
            elif self.player2.total_score > self.player1.total_score:
                return self.player2.name
            else:
                return "Hòa"  # Trường hợp hiếm khi xảy ra: cả hai có cùng điểm
        elif self.player1.total_score >= 15:
            return self.player1.name
        else:
            return self.player2.name
    
class GameManager:
    def __init__(self, algorithm_dir: str):
        self.algorithm_dir = algorithm_dir
        self.players: List[Player] = []
        self.matches: List[Match] = []
        self.current_match_index: int = 0
        self.load_players()
        self.create_matches()
    
    def load_players(self):
        """Load all player algorithms from the Algorithm directory"""
        for file in os.listdir(self.algorithm_dir):
            if file.endswith('.py') and file != 'template.py':
                try:
                    player_name = os.path.splitext(file)[0]
                    file_path = os.path.join(self.algorithm_dir, file)
                    
                    spec = importlib.util.spec_from_file_location(player_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Kiểm tra xem module có hàm giveDecision không
                    if not hasattr(module, 'giveDecision'):
                        print(f"Warning: {file} không có hàm giveDecision, bỏ qua file này")
                        continue
                        
                    # Kiểm tra xem giveDecision có phải là hàm không
                    if not callable(getattr(module, 'giveDecision')):
                        print(f"Warning: {file} có giveDecision nhưng không phải là hàm, bỏ qua file này")
                        continue
                    
                    self.players.append(Player(name=player_name, module=module))
                    
                except Exception as e:
                    print(f"Error loading {file}: {str(e)}")
    
    def create_matches(self):
        """Create matches between all players"""
        self.matches = []
        for i, player1 in enumerate(self.players):
            for player2 in self.players[i+1:]:
                # Reset điểm số trước khi tạo trận mới
                player1.total_score = 0
                player2.total_score = 0
                self.matches.append(Match(player1, player2, []))
    
    def get_decision_with_timeout(self, player: Player, history: List[Dict[str, Tuple[Decision, int]]]) -> Decision:
        """Get player's decision with 10 second timeout"""
        def run_player_decision():
            return player.module.giveDecision(history)
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                future = executor.submit(run_player_decision)
                decision = future.result(timeout=10)
                if decision not in ['C', 'D']:
                    raise ValueError("Invalid decision")
                return decision
            except (TimeoutError, ValueError, Exception) as e:
                return 'TIMEOUT'
    
    def calculate_scores(self, decision1: Decision, decision2: Decision) -> Tuple[int, int]:
        """Calculate scores based on decisions"""
        if decision1 == 'TIMEOUT':
            return 0, 5
        if decision2 == 'TIMEOUT':
            return 5, 0
            
        if decision1 == 'C' and decision2 == 'C':
            return 3, 3
        elif decision1 == 'C' and decision2 == 'D':
            return 0, 5
        elif decision1 == 'D' and decision2 == 'C':
            return 5, 0
        else:  # Both defect
            return 1, 1
    
    def play_turn(self) -> Optional[Match]:
        """Play one turn of the current match"""
        if self.current_match_index >= len(self.matches):
            return None
            
        current_match = self.matches[self.current_match_index]
        if current_match.is_finished():
            if current_match.winner is None:
                winner_name = current_match.get_winner()
                current_match.winner = winner_name
                # Cập nhật số trận thắng
                if winner_name == current_match.player1.name:
                    current_match.player1.matches_won += 1
                elif winner_name == current_match.player2.name:
                    current_match.player2.matches_won += 1
            
            # Reset điểm số cho trận kế tiếp
            if self.current_match_index + 1 < len(self.matches):
                next_match = self.matches[self.current_match_index + 1]
                next_match.player1.total_score = 0
                next_match.player2.total_score = 0
            
            self.current_match_index += 1  # Tăng current_match_index
            
            return current_match
            
        # Get decisions
        decision1 = self.get_decision_with_timeout(current_match.player1, current_match.history)
        decision2 = self.get_decision_with_timeout(current_match.player2, current_match.history)
        
        # Calculate scores
        score1, score2 = self.calculate_scores(decision1, decision2)
        current_match.player1.total_score += score1
        current_match.player2.total_score += score2
        
        # Update history
        current_match.history.append({
            current_match.player1.name: (decision1, current_match.player1.total_score),
            current_match.player2.name: (decision2, current_match.player2.total_score)
        })
        
        # Kiểm tra kết thúc trận sau khi cập nhật điểm
        if current_match.is_finished():
            winner_name = current_match.get_winner()
            current_match.winner = winner_name
            # Cập nhật số trận thắng
            if winner_name == current_match.player1.name:
                current_match.player1.matches_won += 1
            elif winner_name == current_match.player2.name:
                current_match.player2.matches_won += 1
        
        return current_match
    
    def get_rankings(self) -> List[Tuple[str, int, int]]:
        """Get current rankings of all players with matches won
        Returns:
            List[Tuple[str, int, int]]: List of (player_name, total_score, matches_won)
        """
        rankings = [(p.name, p.total_score, p.matches_won) for p in self.players]
        return sorted(rankings, key=lambda x: (x[2], x[1]), reverse=True)  # Sắp xếp theo số trận thắng, sau đó theo điểm
    
    def is_tournament_finished(self) -> bool:
        """Kiểm tra xem giải đấu đã kết thúc chưa"""
        return self.current_match_index >= len(self.matches)
    
    def get_upcoming_matches(self) -> List[Tuple[str, str]]:
        """Get list of upcoming matches"""
        # Trả về tất cả các trận, không cắt bớt
        return [(m.player1.name, m.player2.name) for m in self.matches]
    
    def get_current_match(self) -> Optional[Match]:
        """Get current match or None if tournament is finished"""
        if self.current_match_index >= len(self.matches):
            return None
        return self.matches[self.current_match_index]
