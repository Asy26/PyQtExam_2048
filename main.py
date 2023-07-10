import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QLabel, QMessageBox)

ROW = 4
COL = 4

colors_numbers = {
    '0': {'color': QColor(0xcdc1b4),'font': QColor(0xcdc1b4)},
    '2': {'color': QColor(0xeee4da),'font': QColor(0x776e65)},
    '4': {'color': QColor(0xede0c8),'font': QColor(0x776e65)},
    '8': {'color': QColor(0xf2b179),'font': QColor(0xffffff)},
    '16': {'color': QColor(0xf59563),'font': QColor(0xffffff)},
    '32': {'color': QColor(0xf67c5f),'font': QColor(0xffffff)},
    '64': {'color': QColor(0xf65e3b),'font': QColor(0xffffff)},
    '128': {'color': QColor(0xedcf72),'font': QColor(0xffffff)},
    '256': {'color': QColor(0xedcc61),'font': QColor(0xffffff)},
    '512': {'color': QColor(0xedc850),'font': QColor(0xffffff)},
    '1024': {'color': QColor(0xedc53f),'font': QColor(0xffffff)},
    '2048': {'color': QColor(0xedc22e),'font': QColor(0xffffff)}
}


class Game(QWidget):

    def __init__(self):
        # вызов конструктора базового класса и установка начальных значений для переменных
        super().__init__()

        self.isLose = False
        self.isMove = False
        self.succeed = False
        self.palettes = []
        self.labels = []
        self.main_ui()

    def main_ui(self):
        # создает основной интерфейс игры
        self.setWindowTitle('2048')
        self.setGeometry(0, 0, 400, 400)

        layout = QGridLayout()
        layout.setSpacing(5)
        self.setLayout(layout)
        # создается сетка из ROW строк и столбцов
        # в каждую ячейку сетки добавляется виджет QLabel, который будет отображать числа на игровом поле
        for i in range(ROW ** 2):
            label = QLabel('0', self)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(80)
            label.setFixedHeight(80)
            label.setFont(QFont("Arial", 25, QFont.Bold))
            layout.addWidget(label, i // ROW, i % ROW)
            self.labels.append(label)

            pe = QPalette()
            pe.setColor(QPalette.WindowText, colors_numbers['0']['font'])
            label.setAutoFillBackground(True)
            pe.setColor(QPalette.Window, colors_numbers['0']['color'])
            label.setPalette(pe)
            self.palettes.append(pe)
        # случайным образом устанавливаем несколько начальных чисел на игровом поле
        self.random_set_labels(3)

        self.show()

    def reset(self):
        # Сбросить все ячейки на пустые значения '0'
        for i in range(ROW * COL):
            self.set_text_and_color(i, '0', setIsMove=False)
        # Случайным образом заполнить 3 ячейки числами
        self.random_set_labels(3)

    def keyPressEvent(self, e):
        # Проверяем нажатие кнопок управления и сдвигаем сетку
        if e.key() == Qt.Key_Up:
            self.move_grid('up')
        elif e.key() == Qt.Key_Down:
            self.move_grid('down')
        elif e.key() == Qt.Key_Left:
            self.move_grid('left')
        elif e.key() == Qt.Key_Right:
            self.move_grid('right')
        # Если нажата R - начинаем игру сначала
        elif e.key() == Qt.Key_R:
            self.reset()

    def move_grid(self, direction):
        # ход игры
        self.remove_empty_label(direction)
        self.merge_same_label(direction)
        if self.isLose:
            self.game_over()
        if self.succeed:
            self.game_over_win()
        if self.isMove:
            self.isMove = False
            self.random_set_labels(1)

    def remove_empty_label(self, direction):
        # удаление пустых полей в зависимости от направления сдвига
        self.isLose = True
        if direction == 'right':
            for i in range(ROW):
                row_point = []
                for j in range(COL - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = COL - 1
                for text in row_point:
                    self.set_text_and_color(i * ROW + j, text)
                    j -= 1
                while j != -1:
                    self.set_text_and_color(i * ROW + j, '0')
                    j -= 1
        elif direction == 'left':
            for i in range(ROW):
                row_point = []
                for j in range(COL):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = 0
                for text in row_point:
                    self.set_text_and_color(i * ROW + j, text)
                    j += 1
                while j != COL:
                    self.set_text_and_color(i * ROW + j, '0')
                    j += 1
        elif direction == 'up':
            for j in range(COL):
                row_point = []
                for i in range(ROW):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = 0
                for text in row_point:
                    self.set_text_and_color(i * ROW + j, text)
                    i += 1
                while i != ROW:
                    self.set_text_and_color(i * ROW + j, '0')
                    i += 1
        elif direction == 'down':
            for j in range(COL):
                col_point = []
                for i in range(ROW - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        col_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = ROW - 1
                for text in col_point:
                    self.set_text_and_color(i * ROW + j, text)
                    i -= 1
                while i != -1:
                    self.set_text_and_color(i * ROW + j, '0')
                    i -= 1

    def merge_same_label(self, direction):
        # объединение полей с одинаковыми значениями
        if direction == 'right':
            for j in range(ROW):
                for i in range(COL - 1, 0, -1):
                    right_label = self.labels[j * ROW + i]
                    left_label = self.labels[j * ROW + i - 1]
                    if right_label.text() == left_label.text():
                        num = int(right_label.text())
                        self.finished_move(j * ROW + i, num * 2)
                        self.set_text_and_color(j * ROW + i, str(num * 2))
                        for k in range(i - 1, 0, -1):
                            self.set_text_and_color(j * ROW + k, self.labels[j * ROW + k - 1].text())
                        self.set_text_and_color(j * ROW + 0, '0')
                        break
        elif direction == 'left':
            for j in range(ROW):
                for i in range(COL - 1):
                    right_label = self.labels[j * ROW + i + 1]
                    left_label = self.labels[j * ROW + i]
                    if right_label.text() == left_label.text():
                        num = int(left_label.text())
                        self.finished_move(j * ROW + i, num * 2)
                        self.set_text_and_color(j * ROW + i, str(num * 2))
                        for k in range(i + 1, COL - 1):
                            self.set_text_and_color(j * ROW + k, self.labels[j * ROW + k + 1].text())
                        self.set_text_and_color(j * ROW + COL - 1, '0')
                        break
        elif direction == 'down':
            for i in range(COL):
                for j in range(ROW - 1, 0, -1):
                    up_label = self.labels[(j - 1) * ROW + i]
                    down_label = self.labels[j * ROW + i]
                    if up_label.text() == down_label.text():
                        num = int(down_label.text())
                        self.finished_move(j * ROW + i, num * 2)
                        self.set_text_and_color(j * ROW + i, str(num * 2))
                        for k in range(j - 1, 0, -1):
                            self.set_text_and_color(k * ROW + i, self.labels[(k - 1) * ROW + i].text())
                        self.set_text_and_color(0 * ROW + i, '0')
                        break
        elif direction == 'up':
            for i in range(COL):
                for j in range(ROW - 1):
                    up_label = self.labels[j * ROW + i]
                    down_label = self.labels[(j + 1) * ROW + i]
                    if up_label.text() == down_label.text():
                        num = int(up_label.text())
                        self.finished_move(j * ROW + i, num * 2)
                        self.set_text_and_color(j * ROW + i, str(num * 2))
                        for k in range(j + 1, ROW - 1):
                            self.labels[k * ROW + i].setText(self.labels[(k + 1) * ROW + i].text())
                            self.set_text_and_color(k * ROW + i, self.labels[(k + 1) * ROW + i].text())
                        self.set_text_and_color((COL - 1) * ROW + i, '0')
                        break

    def random_set_labels(self, nums):
        # установка случайных значений в поля сетки
        empty_grids = self.get_empty_grid()
        num_str = '222448'
        for _ in range(nums):
            num = random.choice(num_str)
            label_index = random.choice(empty_grids)
            self.set_text_and_color(label_index, num, setIsMove=False)

    def get_empty_grid(self):
        # возвращает список пустых полей в сетке
        results = [index for index, labels in enumerate(self.labels) if labels.text() == '0']
        return results

    def set_text_and_color(self, index, num, setIsMove=True):
        if setIsMove:
            pre_text = self.labels[index].text()
            if pre_text != num:
                self.isMove = True

        self.labels[index].setText(num)
        self.palettes[index].setColor(QPalette.WindowText, colors_numbers[num]['font'])
        self.palettes[index].setColor(QPalette.Window, colors_numbers[num]['color'])
        self.labels[index].setPalette(self.palettes[index])

    def finished_move(self, index, num):
        if num == 2048:
            self.succeed = True
        self.isLose = False

    def game_over(self):
        button = QMessageBox.question(self, "Игра окончена",
                                      "Ходов больше нет! Хотите начать заново?",
                                      QMessageBox.Ok |
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.reset()

    def game_over_win(self):
        button = QMessageBox.question(self, "Поздравляем",
                                      "Вы собрали 2048! Хотите начать заново?",
                                      QMessageBox.Ok |
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
