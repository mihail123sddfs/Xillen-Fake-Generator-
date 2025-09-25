import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from faker import Faker
import csv

class XillenFakeDataGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xillen Fake Data Generator")
        self.setMinimumSize(800, 500)
        self.faker = Faker()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Xillen Fake Data Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; color: #7ecfff; margin-bottom: 10px;")
        layout.addWidget(title)

        row = QVBoxLayout()
        self.count_box = QSpinBox()
        self.count_box.setRange(1, 1000)
        self.count_box.setValue(10)
        self.count_box.setPrefix("Количество строк: ")
        layout.addWidget(self.count_box)

        self.btn_generate = QPushButton("Сгенерировать")
        self.btn_generate.clicked.connect(self.generate)
        layout.addWidget(self.btn_generate)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Имя", "Email", "Адрес", "Телефон", "Карта"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.btn_save = QPushButton("Сохранить в CSV")
        self.btn_save.clicked.connect(self.save_csv)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def generate(self):
        count = self.count_box.value()
        self.table.setRowCount(count)
        for i in range(count):
            name = self.faker.name()
            email = self.faker.email()
            address = self.faker.address().replace('\n', ', ')
            phone = self.faker.phone_number()
            card = self.faker.credit_card_number(card_type=None)
            for j, val in enumerate([name, email, address, phone, card]):
                self.table.setItem(i, j, QTableWidgetItem(val))
        self.btn_save.setEnabled(True)

    def save_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить CSV", "fake_data.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Имя", "Email", "Адрес", "Телефон", "Карта"])
                for i in range(self.table.rowCount()):
                    row = [self.table.item(i, j).text() for j in range(self.table.columnCount())]
                    writer.writerow(row)
            QMessageBox.information(self, "Успех", f"Сохранено {self.table.rowCount()} строк в {path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = XillenFakeDataGenerator()
    win.show()
    sys.exit(app.exec_())
