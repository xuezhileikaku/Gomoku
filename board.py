# 负责棋盘绘制、棋子放置。
import pygame

# 常量定义
BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 30
WIDTH = HEIGHT = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (238, 154, 73)


class Board:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self):
        """绘制棋盘"""
        self.screen.fill(BOARD_COLOR)
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, BLACK, (MARGIN, MARGIN + i * CELL_SIZE),
                             (WIDTH - MARGIN, MARGIN + i * CELL_SIZE))
            pygame.draw.line(self.screen, BLACK, (MARGIN + i * CELL_SIZE, MARGIN),
                             (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN))

        # 绘制星位
        for p in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            pygame.draw.circle(self.screen, BLACK,
                               (MARGIN + p[0] * CELL_SIZE, MARGIN + p[1] * CELL_SIZE), 5)

    def draw_pieces(self, board):
        """绘制所有棋子"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 1:
                    color = BLACK
                elif board[i][j] == 2:
                    color = WHITE
                else:
                    continue
                pos = (MARGIN + j * CELL_SIZE, MARGIN + i * CELL_SIZE)
                pygame.draw.circle(self.screen, color, pos, CELL_SIZE // 2 - 2)
