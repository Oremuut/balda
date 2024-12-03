from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, \
    QGraphicsView


class GameView(QGraphicsView):
    def __init__(self, model, score_labels):
        super().__init__()
        self.model = model
        self.score_labels = score_labels
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.init_ui()

        self.selected_cells = []
        self.is_dragging = False

    def init_ui(self):
        self.setFixedSize(502, 502)
        self.scene.setSceneRect(0, 0, 500, 500)

        self.cells = []
        for y in range(5):
            row = []
            for x in range(5):
                rect = QGraphicsRectItem(x * 100, y * 100, 100, 100)
                rect.setBrush(QBrush(QColor("white")))
                rect.setPen(QColor("black"))
                self.scene.addItem(rect)

                if self.model.board[y][x]:
                    text = QGraphicsTextItem(self.model.board[y][x])
                    text.setDefaultTextColor(Qt.black)
                    text.setPos(x * 100 + 40, y * 100 + 40)
                    self.scene.addItem(text)

                row.append((rect, None))
            self.cells.append(row)

    def mousePressEvent(self, event):
        x = int(event.x() // 100)
        y = int(event.y() // 100)

        if 0 <= x < 5 and 0 <= y < 5:
            if self.model.board[y][x] == "":
                self.handle_letter_input(x, y)
            else:
                self.is_dragging = True
                self.selected_cells = [(x, y)]
                self.update_selection_visual()

    def mouseMoveEvent(self, event):
        if not self.is_dragging:
            return

        x = int(event.x() // 100)
        y = int(event.y() // 100)

        if 0 <= x < 5 and 0 <= y < 5 and (x, y) not in self.selected_cells:
            if self.model.board[y][x] != "":
                self.selected_cells.append((x, y))
                self.update_selection_visual()

    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.finalize_word()

    def handle_letter_input(self, x, y):
        letter, ok = QInputDialog.getText(self, "Введите букву", "Введите букву для клетки:")
        if not ok or len(letter) != 1 or not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод! Введите одну букву.")
            return

        letter = letter.upper()
        try:
            self.model.add_letter(x, y, letter)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return

        self.refresh_board()

    def finalize_word(self):
        word = "".join(self.model.board[y][x] for x, y in self.selected_cells)
        if len(word) == 1:
            self.selected_cells = []
            self.refresh_board()
            return
        if word:
            try:
                self.model.add_word(word)
                QMessageBox.information(self, "Слово принято", f"Вы составили слово \"{word}\"!")
                self.update_scores()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

        self.selected_cells = []
        self.refresh_board()

    def update_selection_visual(self):
        for x, y in self.selected_cells:
            rect, _ = self.cells[y][x]
            rect.setBrush(QBrush(QColor("lightblue")))

    def refresh_board(self):
        self.scene.clear()
        self.init_ui()

    def update_scores(self):
        self.score_labels[0].setText(f"Игрок 1: {self.model.scores[0]} очков")
        self.score_labels[1].setText(f"Игрок 2: {self.model.scores[1]} очков")
