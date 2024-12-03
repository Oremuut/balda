import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from balda_model import GameModel
from balda_view import GameView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра Балда")
        self.setGeometry(100, 100, 520, 650)

        self.model = GameModel()

        self.player1_score_label = QLabel("Игрок 1: 0 очков")
        self.player2_score_label = QLabel("Игрок 2: 0 очков")
        self.current_player_label = QLabel("Ходит: Игрок 1")
        self.player1_score_label.setAlignment(Qt.AlignCenter)
        self.player2_score_label.setAlignment(Qt.AlignCenter)
        self.current_player_label.setAlignment(Qt.AlignCenter)

        self.pass_button = QPushButton("Пропустить ход")
        self.pass_button.clicked.connect(self.handle_pass_turn)

        self.game_view = GameView(self.model, [self.player1_score_label, self.player2_score_label])

        layout = QVBoxLayout()
        layout.addWidget(self.player1_score_label)
        layout.addWidget(self.player2_score_label)
        layout.addWidget(self.current_player_label)
        layout.addWidget(self.game_view)
        layout.addWidget(self.pass_button)

        self.setLayout(layout)

    def handle_pass_turn(self):
        try:
            self.model.pass_turn()
            self.update_turn_display()
        except ValueError as e:
            QMessageBox.information(self, "Игра завершена", str(e))
            self.end_game()

    def end_game(self):
        self.pass_button.setDisabled(True)
        self.game_view.setDisabled(True)

    def update_turn_display(self):
        current_player = "Игрок 1" if self.model.current_player == 0 else "Игрок 2"
        self.current_player_label.setText(f"Ходит: {current_player}")

        self.player1_score_label.setText(f"Игрок 1: {self.model.scores[0]} очков")
        self.player2_score_label.setText(f"Игрок 2: {self.model.scores[1]} очков")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
