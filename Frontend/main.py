import os
import sys
import pygame
from typing import Optional
from .constants import *
from .ui_components import Button, MatchList, Leaderboard, MatchDisplay
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Backend.game_manager import GameManager
from Backend.logger import GameLogger

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cooperate and Defect Game")
        
        self.clock = pygame.time.Clock()
        
        # Khởi tạo font với Unicode support
        if FONT_PATH:
            self.font = pygame.font.Font(FONT_PATH, NORMAL_FONT_SIZE)
            self.title_font = pygame.font.Font(FONT_PATH, TITLE_FONT_SIZE)
        else:
            self.font = pygame.font.SysFont('arial', NORMAL_FONT_SIZE)
            self.title_font = pygame.font.SysFont('arial', TITLE_FONT_SIZE)
        
        # Initialize components
        self.match_list = MatchList(PADDING, PADDING, 
                                  SIDEBAR_WIDTH - 2*PADDING, 
                                  WINDOW_HEIGHT - 2*PADDING)
        
        self.leaderboard = Leaderboard(WINDOW_WIDTH - SIDEBAR_WIDTH + PADDING, 
                                     PADDING,
                                     SIDEBAR_WIDTH - 2*PADDING, 
                                     WINDOW_HEIGHT - 2*PADDING)
        
        self.match_display = MatchDisplay(SIDEBAR_WIDTH + PADDING, 
                                        PADDING,
                                        MAIN_AREA_WIDTH - 2*PADDING, 
                                        WINDOW_HEIGHT - 2*PADDING - BUTTON_HEIGHT - PADDING)
        
        # Tạo hai nút cạnh nhau
        button_total_width = 2 * BUTTON_WIDTH + BUTTON_SPACING
        button_start_x = SIDEBAR_WIDTH + (MAIN_AREA_WIDTH - button_total_width)//2
        button_y = WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING
        
        self.next_turn_button = Button(button_start_x, button_y,
                                     BUTTON_WIDTH, BUTTON_HEIGHT, "Lượt tiếp")
        
        self.next_match_button = Button(button_start_x + BUTTON_WIDTH + BUTTON_SPACING,
                                      button_y, BUTTON_WIDTH, BUTTON_HEIGHT,
                                      "Trận tiếp")
        self.next_match_button.active = False  # Bắt đầu với trận đầu tiên
        
        # Initialize game logic
        self.game_manager = GameManager("Algorithm")
        self.logger = GameLogger("logs")
        
        # Update initial state
        self._update_display_state()
    
    def _update_display_state(self):
        """Update all UI components with current game state"""
        current_match = self.game_manager.get_current_match()
        upcoming_matches = self.game_manager.get_upcoming_matches()
        rankings = self.game_manager.get_rankings()
        is_tournament_finished = self.game_manager.is_tournament_finished()
        
        # Cập nhật danh sách trận và bảng xếp hạng
        self.match_list.update_matches(upcoming_matches, 
                                     self.game_manager.current_match_index)
        self.leaderboard.update_rankings(rankings, is_tournament_finished)
        
        # Cập nhật hiển thị trận đấu
        if is_tournament_finished:
            self.match_display.update_match(None, None, True)
            # Disable cả hai nút khi giải đấu kết thúc
            self.next_turn_button.active = False
            self.next_match_button.active = False
        elif current_match:
            match_dict = {
                'player1': current_match.player1,
                'player2': current_match.player2,
                'history': current_match.history
            }
            self.match_display.update_match(match_dict, current_match.winner if current_match.is_finished() else None)
            
            # Cập nhật trạng thái nút dựa vào trạng thái trận đấu
            if current_match.is_finished():
                self.next_turn_button.active = False
                self.next_match_button.active = self.game_manager.current_match_index < len(self.game_manager.matches) - 1
            else:
                self.next_turn_button.active = True
                self.next_match_button.active = False
        else:
            self.match_display.update_match(None)
            self.next_turn_button.active = False
            self.next_match_button.active = False
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Xử lý hover và click cho cả hai nút
            self.next_turn_button.handle_event(event)
            self.next_match_button.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.next_turn_button.rect.collidepoint(mouse_pos):
                        if self.next_turn_button.active:
                            self._handle_next_turn()
                    
                    elif self.next_match_button.rect.collidepoint(mouse_pos):
                        if self.next_match_button.active:
                            self._handle_next_match()
        
        return True
    
    def _handle_next_turn(self):
        """Handle next turn button click"""
        current_match = self.game_manager.play_turn()
        
        # In thông tin lượt đấu
        if current_match:
            p1_decision = current_match.history[-1][current_match.player1.name][0]
            p2_decision = current_match.history[-1][current_match.player2.name][0]
            print(f"\nLượt {len(current_match.history)}:")
            print(f"{current_match.player1.name}: {p1_decision} ({current_match.player1.total_score} điểm)")
            print(f"{current_match.player2.name}: {p2_decision} ({current_match.player2.total_score} điểm)")
            
            if current_match.is_finished():
                print(f"\n=== Kết thúc trận đấu! ===")
                print(f"Điểm số cuối cùng:")
                print(f"{current_match.player1.name}: {current_match.player1.total_score} điểm")
                print(f"{current_match.player2.name}: {current_match.player2.total_score} điểm")
                print(f"Người chiến thắng: {current_match.winner}")
                print("=" * 30)
                
                # Log kết quả trận đấu
                self.logger.log_match(
                    current_match.player1.name,
                    current_match.player2.name,
                    current_match.history,
                    current_match.winner
                )
        
        self._update_display_state()
    
    def _handle_next_match(self):
        """Handle next match button click"""
        # Kiểm tra xem có trận tiếp theo không
        if self.game_manager.current_match_index < len(self.game_manager.matches) - 1:
            # Reset điểm của trận tiếp theo
            next_match = self.game_manager.matches[self.game_manager.current_match_index + 1]
            next_match.player1.total_score = 0
            next_match.player2.total_score = 0
            
            # Chuyển sang trận tiếp theo
            self.game_manager.current_match_index += 1
            current_match = self.game_manager.get_current_match()
            
            if current_match:
                print(f"\n=== Bắt đầu trận mới ===")
                print(f"{current_match.player1.name} vs {current_match.player2.name}")
                print("=" * 30)
                
                # Disable nút trận tiếp, enable nút lượt tiếp
                self.next_match_button.active = False
                self.next_turn_button.active = True
            else:
                # Giải đấu kết thúc
                print(f"\n=== Kết thúc giải đấu! ===")
                print("=" * 30)
                
                # In bảng điểm cuối cùng
                rankings = self.game_manager.get_rankings()
                self.leaderboard.update_rankings(rankings, True)
                
                # Disable cả hai nút
                self.next_match_button.active = False
                self.next_turn_button.active = False
        
        self._update_display_state()
    
    def draw(self):
        """Draw all game components"""
        self.screen.fill(WHITE)
        
        self.match_list.draw(self.screen, self.font)
        self.leaderboard.draw(self.screen, self.font)
        self.match_display.draw(self.screen, self.font)
        
        self.next_turn_button.draw(self.screen, self.font)
        self.next_match_button.draw(self.screen, self.font)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
