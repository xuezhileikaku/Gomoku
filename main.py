# 这个五子棋游戏包含以下功能：
#
# 游戏模式选择：
# 双人对战模式（玩家轮流下棋）
# 人机对战模式（AI使用随机算法）
#
# 主要游戏功能：
# 棋盘绘制和棋子显示
# 鼠标点击落子
# 胜利条件判断
# 游戏结束提示
# 按R键重新开始游戏
#
# AI功能：
# 当前使用简单随机算法
# 可以扩展为更智能的算法（如基于评分系统）
#
# 界面特性：
# 传统棋盘布局
# 星位标记
# 清晰的胜负提示
#
# 操作说明：
# 启动游戏后选择游戏模式
# 在棋盘上点击鼠标左键落子
# 当一方连成五子时游戏结束
# 按R键可以随时重新开始游戏

import pygame
from game import Gomoku

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 660, 660  # 窗口大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("五子棋")

# 启动游戏
game = Gomoku(screen)
game.run()


