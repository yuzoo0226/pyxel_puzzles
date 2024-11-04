import pyxel
import random

# ゲーム設定
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160
GRID_SIZE = 8
BOARD_WIDTH = SCREEN_WIDTH // GRID_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# ブロックの形を定義
SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # 四角形
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # 棒
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # ジグザグ
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T字
]


class TetrisGame:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_shape = random.choice(SHAPES)
        self.current_x = BOARD_WIDTH // 2
        self.current_y = 0
        self.game_over = False

    def can_move(self, dx, dy):
        for x, y in self.current_shape:
            new_x = self.current_x + x + dx
            new_y = self.current_y + y + dy
            if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                return False
            if new_y >= 0 and self.board[new_y][new_x] != 0:
                return False
        return True

    def place_shape(self):
        for x, y in self.current_shape:
            self.board[self.current_y + y][self.current_x + x] = 1
        self.clear_lines()
        self.current_shape = random.choice(SHAPES)
        self.current_x = BOARD_WIDTH // 2
        self.current_y = 0
        if not self.can_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.board = new_board

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        if pyxel.btnp(pyxel.KEY_LEFT) and self.can_move(-1, 0):
            self.current_x -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.can_move(1, 0):
            self.current_x += 1
        if pyxel.btnp(pyxel.KEY_DOWN) and self.can_move(0, 1):
            self.current_y += 1

        if pyxel.frame_count % 30 == 0:  # 自動で下に移動
            if self.can_move(0, 1):
                self.current_y += 1
            else:
                self.place_shape()

    def draw(self):
        pyxel.cls(0)
        # ボードを描画
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != 0:
                    pyxel.rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, 11)
        # 現在のブロックを描画
        for x, y in self.current_shape:
            draw_x = (self.current_x + x) * GRID_SIZE
            draw_y = (self.current_y + y) * GRID_SIZE
            pyxel.rect(draw_x, draw_y, GRID_SIZE, GRID_SIZE, 8)
        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "GAME OVER! Press R to Restart", 7)


TetrisGame()
