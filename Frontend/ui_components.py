import pygame
from typing import List, Tuple, Dict, Optional
from .constants import *

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = True
        self.hovered = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.active:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                return True
        return False
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        # Chọn màu dựa trên trạng thái
        if not self.active:
            color = BUTTON_DISABLED_COLOR
        elif self.hovered:
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_ENABLED_COLOR
            
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.active and self.rect.collidepoint(pos)

class MatchList:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.matches: List[Tuple[str, str]] = []
        self.current_index = 0
    
    def update_matches(self, matches: List[Tuple[str, str]], current_index: int):
        self.matches = matches
        self.current_index = current_index
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        title = font.render("Upcoming Matches", True, BLACK)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        y = self.rect.y + 50
        for i, (p1, p2) in enumerate(self.matches):
            color = BLUE if i == self.current_index else BLACK
            text = font.render(f"{p1} vs {p2}", True, color)
            surface.blit(text, (self.rect.x + 10, y))
            y += 30

class Leaderboard:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.rankings: List[Tuple[str, int, int]] = []  # (name, score, matches_won)
        self.show_final = False
        # Tạo font monospace cho bảng xếp hạng
        if MONO_FONT_PATH:
            self.mono_font = pygame.font.Font(MONO_FONT_PATH, LEADERBOARD_FONT_SIZE)
        else:
            self.mono_font = pygame.font.SysFont('courier', LEADERBOARD_FONT_SIZE)
    
    def update_rankings(self, rankings: List[Tuple[str, int, int]], is_final: bool = False):
        self.rankings = rankings
        self.show_final = is_final
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # Vẽ tiêu đề bằng font thường
        title = "BẢNG XẾP HẠNG CUỐI CÙNG" if self.show_final else "Bảng xếp hạng"
        title_surface = font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.y + 10)
        surface.blit(title_surface, title_rect)
        
        # Vẽ header bằng font monospace
        header = "┌────┬──────────┬───────┐"
        header_surface = self.mono_font.render(header, True, BLACK)
        surface.blit(header_surface, (self.rect.x + 10, self.rect.y + 40))
        
        header = "│Hạng│   Tên    │ Thắng │"
        header_surface = self.mono_font.render(header, True, BLACK)
        surface.blit(header_surface, (self.rect.x + 10, self.rect.y + 55))
        
        header = "├────┼──────────┼───────┤"
        header_surface = self.mono_font.render(header, True, BLACK)
        surface.blit(header_surface, (self.rect.x + 10, self.rect.y + 70))
        
        # Vẽ các người chơi
        y = self.rect.y + 85
        for i, (name, score, matches_won) in enumerate(self.rankings, 1):
            color = GREEN if self.show_final and i == 1 else BLACK
            # Đảm bảo tên không quá dài và căn lề trái
            name = name[:8].ljust(8)
            text = f"│ {i:2d} │ {name} │  {matches_won:2d}   │"
            text_surface = self.mono_font.render(text, True, color)
            surface.blit(text_surface, (self.rect.x + 10, y))
            y += 20  # Giảm khoảng cách giữa các dòng
        
        # Vẽ đường kẻ cuối cùng
        if self.rankings:
            footer = "└────┴──────────┴───────┘"
            footer_surface = self.mono_font.render(footer, True, BLACK)
            surface.blit(footer_surface, (self.rect.x + 10, y))

class MatchDisplay:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.current_match: Optional[Dict] = None
        self.history_surface = pygame.Surface((width - 20, height - 100))
        self.winner: Optional[str] = None
        self.show_final = False
    
    def update_match(self, match: Optional[Dict], winner: Optional[str] = None, is_final: bool = False):
        self.current_match = match
        self.winner = winner
        self.show_final = is_final
        self._update_history_surface()
    
    def _update_history_surface(self):
        if not self.current_match and not self.show_final:
            return
            
        self.history_surface.fill(WHITE)
        font = pygame.font.Font(FONT_PATH, NORMAL_FONT_SIZE) if FONT_PATH else pygame.font.SysFont('arial', NORMAL_FONT_SIZE)
        
        y = 10
        
        if self.show_final:
            # Hiển thị thông báo kết thúc giải đấu
            end_text = "=== GIẢI ĐẤU ĐÃ KẾT THÚC! ==="
            text_surface = font.render(end_text, True, GREEN)
            text_rect = text_surface.get_rect(centerx=self.history_surface.get_width()//2)
            self.history_surface.blit(text_surface, (text_rect.x, y))
            y += 40
            
            # Hiển thị hướng dẫn
            guide_text = "Xem bảng xếp hạng cuối cùng ở bên phải"
            text_surface = font.render(guide_text, True, BLACK)
            text_rect = text_surface.get_rect(centerx=self.history_surface.get_width()//2)
            self.history_surface.blit(text_surface, (text_rect.x, y))
            return
        
        # Hiển thị thông báo kết thúc nếu có
        if self.winner:
            end_text = f"=== TRẬN ĐẤU KẾT THÚC! {self.winner} CHIẾN THẮNG! ==="
            text_surface = font.render(end_text, True, GREEN)
            self.history_surface.blit(text_surface, (10, y))
            y += 40  # Thêm khoảng cách sau thông báo
        
        # Hiển thị lịch sử các lượt
        for i, turn in enumerate(self.current_match['history']):
            for player, (decision, score) in turn.items():
                text = f"Lượt {i+1}: {player} chọn {decision} (Điểm: {score})"
                text_surface = font.render(text, True, BLACK)
                self.history_surface.blit(text_surface, (10, y))
                y += 25
            y += 5
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        if not self.current_match and not self.show_final:
            text = font.render("No match in progress", True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
            return
        
        # Draw match title
        if self.current_match:
            p1 = self.current_match['player1'].name
            p2 = self.current_match['player2'].name
            title = font.render(f"{p1} vs {p2}", True, BLACK)
            surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw history
        history_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 80,
                                 self.rect.width - 20, self.rect.height - 100)
        surface.blit(self.history_surface, history_rect)
