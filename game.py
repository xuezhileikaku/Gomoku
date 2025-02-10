# 负责游戏逻辑，包括玩家 / AI落子、胜负判断

import pygame
import pygame.mixer
import random
from board import Board
from ai import AI

class Gomoku:
    def __init__(self, screen):
        self.screen = screen
        self.board = [[0] * 15 for _ in range(15)]
        self.current_player = 1
        self.board_drawer = Board(screen)
        self.game_over = False
        self.ai = AI(self.board)
        self.running = True
        self.history = []
        self.undo_count = {1: 0, 2: 0}


        # 🎵 加载背景音乐 & 音效
        pygame.mixer.init()
        pygame.mixer.music.load("assets/bg_music.mp3")
        pygame.mixer.music.play(-1)
        self.sound_place = pygame.mixer.Sound("assets/place.wav")
        self.sound_win = pygame.mixer.Sound("assets/win.wav")

    def check_win(self, row, col):
        """检查是否获胜"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            x, y = row + dx, col + dy
            while 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.current_player:
                count += 1
                x += dx
                y += dy
            x, y = row - dx, col - dy
            while 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.current_player:
                count += 1
                x -= dx
                y -= dy
            if count >= 5:
                return True
        return False

    def handle_click(self, pos):
        """处理点击"""
        if self.game_over:
            return

        x, y = pos
        col = round((x - 30) / 40)
        row = round((y - 30) / 40)

        if 0 <= row < 15 and 0 <= col < 15 and self.board[row][col] == 0:
            self.history.append((row, col, self.current_player))
            self.animate_piece(row, col, self.current_player)
            self.board[row][col] = self.current_player
            self.sound_place.play()

            if self.check_win(row, col):
                self.game_over = True
                self.show_victory_message(f"{'黑棋' if self.current_player == 1 else '白棋'} 获胜！")
            else:
                self.current_player = 3 - self.current_player

            if self.current_player == 2 and not self.game_over:
                ai_row, ai_col = self.ai.find_best_move(2)
                self.history.append((ai_row, ai_col, 2))
                self.animate_piece(ai_row, ai_col, 2)
                self.board[ai_row][ai_col] = 2
                if self.check_win(ai_row, ai_col):
                    self.game_over = True
                    self.show_victory_message("白棋 获胜！")
                else:
                    self.current_player = 1

    def animate_piece(self, row, col, player):
        """落子动画"""
        color = (0, 0, 0) if player == 1 else (255, 255, 255)
        max_radius = 18
        for r in range(2, max_radius, 2):
            self.board_drawer.draw_board()
            self.board_drawer.draw_pieces(self.board)
            pygame.draw.circle(self.screen, color, (30 + col * 40, 30 + row * 40), r)
            pygame.display.flip()
            pygame.time.delay(20)

    def undo(self):
        """悔棋（每人最多 3 次）"""
        if self.undo_count[self.current_player] >= 3:
            print(f"⚠️ {self.current_player} 悔棋次数已用完！")
            return

        if self.history:
            last_move = self.history.pop()
            self.board[last_move[0]][last_move[1]] = 0
            self.current_player = last_move[2]
            self.undo_count[self.current_player] += 1

            if self.current_player == 2 and self.history:
                last_ai_move = self.history.pop()
                self.board[last_ai_move[0]][last_ai_move[1]] = 0
                self.current_player = 1
                self.undo_count[2] += 1

    def show_victory_message(self, message):
        """弹出胜利提示"""
        pygame.mixer.music.stop()
        self.sound_win.play()
        font = pygame.font.Font("assets/LXGWWenKai-Regular.ttf", 50)  # 50 是字号大小
        text_surface = font.render(message, True, (255, 0, 0))
        self.screen.blit(text_surface, (250, 20))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def run(self):
        """主循环"""
        while self.running:
            self.screen.fill((255, 255, 255))
            self.board_drawer.draw_board()
            self.board_drawer.draw_pieces(self.board)
            self.show_current_player()

            if self.game_over:
                winner = "黑方" if self.current_player == 1 else "白方"
                self.show_victory_message(f"{winner}获胜！")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.screen)
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.undo()

        pygame.quit()

    def show_current_player(self):
        """显示当前玩家"""
        font = pygame.font.Font("assets/LXGWWenKai-Regular.ttf", 20)  # 50 是字号大小
        player_text = "当前玩家：黑棋" if self.current_player == 1 else "当前玩家：白棋"
        text_surface = font.render(player_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (450, 20))
