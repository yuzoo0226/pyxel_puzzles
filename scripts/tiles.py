import pyxel
import random

# ゲーム設定
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 180  # ステータスバー用に高さを増加
GRID_SIZE = 20
BOARD_WIDTH = 6
BOARD_HEIGHT = 6

# タイルの模様を定義
TILE_PATTERNS = ["sword", "shield", "potion", "coin", "enemy"]  # 模様の種類

class TilePuzzleGame:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.load_assets()
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def load_assets(self):
        # 各タイルに対応する画像をロード（Pyxelのイメージバンクは最大3つまで）
        for i, pattern in enumerate(TILE_PATTERNS):
            pyxel.images[0].load(i * GRID_SIZE, 0, f"../io/{pattern}.png")

    def reset_game(self):
        self.board = [[random.choice(TILE_PATTERNS) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.selected_tiles = []
        self.is_dragging = False
        self.game_over = False
        self.score = 0
        self.coin_count = 0
        self.coin_threshold = 2

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x = pyxel.mouse_x // GRID_SIZE
            mouse_y = (pyxel.mouse_y - 16) // GRID_SIZE  # ステータスバーを考慮してマウス位置を調整
            if 0 <= mouse_x < BOARD_WIDTH and 0 <= mouse_y < BOARD_HEIGHT:
                if not self.selected_tiles or (mouse_x, mouse_y) != self.selected_tiles[-1]:
                    if not self.selected_tiles or self.is_adjacent(self.selected_tiles[-1], (mouse_x, mouse_y)):
                        if (mouse_x, mouse_y) not in self.selected_tiles:  # 重複して選択しないようにする
                            # 隣接している同じIDを持つタイルのみ選択可能にする
                            if not self.selected_tiles or self.board[mouse_y][mouse_x] == self.board[self.selected_tiles[-1][1]][self.selected_tiles[-1][0]]:
                                self.selected_tiles.append((mouse_x, mouse_y))
                        self.is_dragging = True
        else:
            if self.is_dragging:
                print("Left mouse button released")
                if len(self.selected_tiles) >= 3:  # 3つ以上選択されている場合のみ処理
                    self.score += len(self.selected_tiles)  # スコアを追加
                    for x, y in self.selected_tiles:
                        if self.board[y][x] == "coin":
                            self.coin_count += 1
                        self.board[y][x] = 0  # タイルを削除する
                    self.apply_gravity()  # タイルを下に降ろす
                    self.fill_empty_tiles()  # 空いたタイルに新しいタイルを追加する
                    self.check_coin_count()  # コインのカウントをチェック
                self.selected_tiles = []
                self.is_dragging = False

        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.is_dragging:
            self.check_match()

    def is_adjacent(self, tile1, tile2):
        x1, y1 = tile1
        x2, y2 = tile2
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    def check_match(self):
        if len(self.selected_tiles) < 3:  # 3つ以上選択されている場合のみチェック
            self.selected_tiles = []
            return

        first_tile = self.selected_tiles[0]
        pattern = self.board[first_tile[1]][first_tile[0]]
        if all(self.board[y][x] == pattern for x, y in self.selected_tiles):
            self.score += len(self.selected_tiles)  # スコアを追加
            for x, y in self.selected_tiles:
                if self.board[y][x] == "coin":
                    self.coin_count += 1
                self.board[y][x] = 0  # タイルを消す
            self.apply_gravity()  # タイルを下に降ろす
            self.fill_empty_tiles()  # 空いたタイルに新しいタイルを追加する
            self.check_coin_count()  # コインのカウントをチェック
        self.selected_tiles = []

    def apply_gravity(self):
        # 各列に対してタイルを下に降ろす処理
        for x in range(BOARD_WIDTH):
            # タイルの情報を集めて下に詰める
            column = [self.board[y][x] for y in range(BOARD_HEIGHT) if self.board[y][x] != 0]
            # 空の部分を埋める
            empty_cells = [0] * (BOARD_HEIGHT - len(column))
            # 新しい列を作成
            new_column = empty_cells + column
            # ボードに反映
            for y in range(BOARD_HEIGHT):
                self.board[y][x] = new_column[y]

    def fill_empty_tiles(self):
        # 空のタイルに新しいタイルをランダムに設定
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] == 0:
                    self.board[y][x] = random.choice(TILE_PATTERNS)

    def check_coin_count(self):
        while self.coin_count >= self.coin_threshold:
            print("You collected 50 coins!")
            self.coin_count -= self.coin_threshold

    def draw(self):
        pyxel.cls(0)
        # 現在時刻を右上に表示
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        pyxel.text(SCREEN_WIDTH - 40, 5, current_time, 7)
        # ステータスバーを描画（スコア表示）
        pyxel.rect(0, 0, SCREEN_WIDTH, 16, 5)  # ステータスバーの背景
        pyxel.text(5, 5, f"Score: {self.score}", 7)  # スコアの表示

        # ボードを描画
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != 0:
                    pattern = self.board[y][x]
                    pyxel.blt(x * GRID_SIZE, y * GRID_SIZE + 16, 0, TILE_PATTERNS.index(pattern) * GRID_SIZE, 0, GRID_SIZE, GRID_SIZE, 0)
        # 選択されたタイルをハイライト
        for x, y in self.selected_tiles:
            pyxel.rectb(x * GRID_SIZE, y * GRID_SIZE + 16, GRID_SIZE, GRID_SIZE, 7)
        # マウスの位置を描画
        mouse_x = pyxel.mouse_x // GRID_SIZE
        mouse_y = (pyxel.mouse_y - 16) // GRID_SIZE
        if 0 <= mouse_x < BOARD_WIDTH and 0 <= mouse_y < BOARD_HEIGHT:
            pyxel.rectb(mouse_x * GRID_SIZE, mouse_y * GRID_SIZE + 16, GRID_SIZE, GRID_SIZE, 9)

        # 下部ステータスバーを描画（コインカウント表示）
        pyxel.rect(0, SCREEN_HEIGHT - 16, SCREEN_WIDTH, 16, 5)  # ステータスバーの背景
        pyxel.text(5, SCREEN_HEIGHT - 11, f"Coins: {self.coin_count} / {self.coin_threshold}", 7)  # コインカウントの表示

TilePuzzleGame()
