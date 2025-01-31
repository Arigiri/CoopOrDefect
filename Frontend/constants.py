# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Layout
PADDING = 20
SIDEBAR_WIDTH = 300
MAIN_AREA_WIDTH = WINDOW_WIDTH - 2 * SIDEBAR_WIDTH
HEADER_HEIGHT = 50

# Font sizes
TITLE_FONT_SIZE = 24
HEADER_FONT_SIZE = 24
NORMAL_FONT_SIZE = 18
SMALL_FONT_SIZE = 14
LEADERBOARD_FONT_SIZE = 16  # Font size riêng cho bảng xếp hạng

# Font path
import os
import sys

# Tìm font trong Windows
if sys.platform == 'win32':
    FONT_PATH = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
    MONO_FONT_PATH = os.path.join(os.environ['WINDIR'], 'Fonts', 'consola.ttf')  # Consolas font
else:
    FONT_PATH = None
    MONO_FONT_PATH = None

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_PADDING = 10
BUTTON_SPACING = 20  # Khoảng cách giữa các nút

# Button colors
BUTTON_ENABLED_COLOR = (100, 200, 100)  # Xanh lá nhạt
BUTTON_DISABLED_COLOR = (200, 200, 200)  # Xám
BUTTON_HOVER_COLOR = (150, 255, 150)    # Xanh lá đậm

# Match history
HISTORY_LINE_HEIGHT = 30
MAX_HISTORY_LINES = 10
