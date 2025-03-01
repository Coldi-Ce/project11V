import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget, \
    QMessageBox


class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """
        )
        self.conn.commit()

    def init_ui(self):
        self.stack = QStackedWidget()
        self.login_widget = self.create_login_page()
        self.register_widget = self.create_register_page()
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.setWindowTitle("Вход и Регистрация")
        self.setGeometry(100, 100, 300, 200)

    def create_login_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.login_username = QLineEdit()
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        login_button = QPushButton("Войти")
        register_button = QPushButton("Регистрация")

        layout.addWidget(QLabel("Имя пользователя:"))
        layout.addWidget(self.login_username)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.login_password)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        widget.setLayout(layout)
        return widget

    def create_register_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.register_username = QLineEdit()
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        register_button = QPushButton("Зарегистрироваться")
        back_button = QPushButton("Назад")

        layout.addWidget(QLabel("Имя пользователя:"))
        layout.addWidget(self.register_username)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.register_password)
        layout.addWidget(register_button)
        layout.addWidget(back_button)

        register_button.clicked.connect(self.register)
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        widget.setLayout(layout)
        return widget

    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()

        if user:
            QMessageBox.information(self, "Успех", "Вход выполнен!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")

    def register(self):
        username = self.register_username.text()
        password = self.register_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация выполнена!")
            self.stack.setCurrentIndex(0)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя уже занято")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec())
