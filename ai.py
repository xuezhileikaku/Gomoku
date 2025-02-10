# 用于实现更智能的 AI 策略。

import numpy as np

# 评分表
SCORES = {
    "five": 100000,  # 五连
    "live_four": 10000,  # 活四（两端开口）
    "rush_four": 5000,  # 冲四（单端开口）
    "live_three": 1000,  # 活三
    "sleep_three": 500,  # 眠三
    "live_two": 200,  # 活二
    "sleep_two": 50,  # 眠二
}


class AI:
    def __init__(self, board):
        self.board = board  # 传入棋盘

    def evaluate(self, row, col, player):
        """ 评估当前位置的得分 """
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            line = []
            for i in range(-4, 5):  # 检查 -4 ~ +4 位置
                x, y = row + i * dx, col + i * dy
                if 0 <= x < 15 and 0 <= y < 15:
                    line.append(self.board[x][y])
                else:
                    line.append(-1)

            # 计算该方向上的得分
            total_score += self.get_score(line, player)

        return total_score

    def get_score(self, line, player):
        """ 计算某个方向的分数 """
        line_str = ''.join(map(str, line)).replace("-1", "X")  # 边界外替换为 "X"

        # 进攻得分
        if "11111" in line_str:
            return SCORES["five"]
        elif "011110" in line_str:
            return SCORES["live_four"]
        elif "011112" in line_str or "211110" in line_str:
            return SCORES["rush_four"]
        elif "01110" in line_str:
            return SCORES["live_three"]
        elif "0112" in line_str or "2110" in line_str:
            return SCORES["sleep_three"]
        elif "011" in line_str:
            return SCORES["live_two"]
        elif "02" in line_str or "20" in line_str:
            return SCORES["sleep_two"]

        # 防守得分（翻转角色）
        opponent = 3 - player
        line_str = line_str.replace("1", "X").replace("2", "1").replace("X", "2")  # 翻转
        if "11111" in line_str:
            return SCORES["five"]
        elif "011110" in line_str:
            return SCORES["live_four"]
        elif "011112" in line_str or "211110" in line_str:
            return SCORES["rush_four"]
        elif "01110" in line_str:
            return SCORES["live_three"]
        elif "0112" in line_str or "2110" in line_str:
            return SCORES["sleep_three"]
        elif "011" in line_str:
            return SCORES["live_two"]
        elif "02" in line_str or "20" in line_str:
            return SCORES["sleep_two"]

        return 0

    def find_best_move(self, player):
        """ 寻找最佳落子点 """
        max_score = 0
        best_move = None

        for i in range(15):
            for j in range(15):
                if self.board[i][j] == 0:  # 空位
                    score = self.evaluate(i, j, player)
                    if score > max_score:
                        max_score = score
                        best_move = (i, j)

        return best_move
