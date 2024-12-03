class GameModel:
    def __init__(self):
        self.board = [["" for _ in range(5)] for _ in range(5)]  # Поле 5x5
        self.word_list = set()  # Множество слов, уже использованных в игре
        self.scores = [0, 0]  # Очки игроков
        self.current_player = 0  # Текущий игрок (0 или 1)
        self.pass_count = 0  # Счётчик пропусков хода
        self.init_board()

    def init_board(self):
        # Установим слово "БАЛДА" в центре
        initial_word = "БАЛДА"
        for i, char in enumerate(initial_word):
            self.board[2][i] = char

    def add_letter(self, x, y, letter):
        if self.board[y][x] != "":
            raise ValueError("Клетка уже занята")
        self.board[y][x] = letter

    def is_valid_word(self):
        return True

    def add_word(self, word):
        if not self.is_valid_word():
            raise ValueError("Недопустимое слово")
        if word in self.word_list:
            raise ValueError("Слово уже использовано")

        self.word_list.add(word)
        self.scores[self.current_player] += len(word)
        self.switch_player(True)

    def switch_player(self, reset):
        self.current_player = 1 - self.current_player
        if reset:
            self.pass_count = 0

    def pass_turn(self):
        self.pass_count += 1
        if self.pass_count >= 6:
            raise ValueError("Игра окончена: ничья")
        self.switch_player(False)

    def is_game_over(self):
        for row in self.board:
            if "" in row:
                return False
        return True
