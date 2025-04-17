import os
import wikipedia 
import webbrowser
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QTabWidget, QListWidget, QHBoxLayout, QScrollArea
import sys
languages = {'EN': 'en', 'RU': 'ru', 'DE': 'de', 'FR': 'fr', 'ES': 'es', 'ZH': 'zh', 'JA': 'ja', 'KO': 'ko'}

class WikipediaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'EN'
        wikipedia.set_lang(languages[self.lang])
        self.setWindowTitle("Wikipedia Search (Made by Xeon)")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color:#2e3440;color:#eceff4;")
        self.setWindowIcon(QtGui.QIcon('wiki.ico'))
        self.history = []
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {border: 1px solid #4c566a;}
            QTabBar::tab {background: #3b4252; color: #eceff4; padding: 10px; border: 1px solid #4c566a; border-radius: 5px;}
            QTabBar::tab:selected {background: #81a1c1; color: #2e3440;}
            QTabBar::tab:hover {background: #5e81ac;}
        """)
        main_layout.addWidget(self.tabs)

        self.search_tab = QWidget()
        self.tabs.addTab(self.search_tab, "Search")
        self.init_search_tab()

        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, "History")

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def init_search_tab(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter your query:\n(All results are saved as text files and listed in history)")
        self.label.setFont(QtGui.QFont('Ink Free', 16))
        self.label.setStyleSheet("color:#d8dee9;")
        layout.addWidget(self.label)

        input_layout = QHBoxLayout()

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter search query here")
        self.entry.setFont(QtGui.QFont('Segoe Script', 12))
        self.entry.setStyleSheet("background-color:#3b4252;color:#eceff4;border:1px solid #4c566a;padding:5px;")
        self.entry.returnPressed.connect(self.search_wikipedia)
        input_layout.addWidget(self.entry)

        self.language_menu = QComboBox()
        self.language_menu.addItems(languages.keys())
        self.language_menu.setCurrentText(self.lang)
        self.language_menu.currentTextChanged.connect(self.switch_language)
        self.language_menu.setStyleSheet("""
            QComboBox {background-color:#3b4252;color:#eceff4;border:1px solid #4c566a;padding:5px;}
            QComboBox QAbstractItemView {background-color:#4c566a;color:#eceff4;}
        """)
        input_layout.addWidget(self.language_menu)

        self.search_button = QPushButton("🔎 Search")
        self.search_button.clicked.connect(self.search_wikipedia)
        self.search_button.setStyleSheet("background-color:#81a1c1;color:#2e3440;padding:5px;border-radius:5px;")
        input_layout.addWidget(self.search_button)

        layout.addLayout(input_layout)

        self.text_area = QTextEdit()
        self.text_area.setFont(QtGui.QFont('Segoe Script', 12))
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("background-color:#3b4252;color:#eceff4;border:1px solid #4c566a;padding:10px;")
        layout.addWidget(self.text_area)

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("background-color:#3b4252;border:none;")
        self.scroll_area.setWidgetResizable(True)

        self.button_container = QWidget()
        self.button_layout = QVBoxLayout()
        self.button_container.setLayout(self.button_layout)
        self.scroll_area.setWidget(self.button_container)
        layout.addWidget(self.scroll_area)
        self.scroll_area.setVisible(False)

        self.search_tab.setLayout(layout)

    def init_history_tab(self):
        layout = QVBoxLayout()

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {background-color:#3b4252;color:#eceff4;border:1px solid #4c566a;}
            QListWidget::item {padding:10px;border:1px solid #4c566a;margin:2px;}
            QListWidget::item:selected {background-color:#81a1c1;color:#2e3440;}
        """)
        self.history_list.itemClicked.connect(self.handle_history_click)
        layout.addWidget(self.history_list)

        self.history_text_area = QTextEdit()
        self.history_text_area.setFont(QtGui.QFont('Segoe Script', 12))
        self.history_text_area.setReadOnly(True)
        self.history_text_area.setStyleSheet("background-color:#3b4252;color:#eceff4;border:1px solid #4c566a;padding:10px;")
        layout.addWidget(self.history_text_area)

        self.history_tab.setLayout(layout)

    def switch_language(self, new_lang):
        self.lang = new_lang
        wikipedia.set_lang(languages[self.lang])

    def search_wikipedia(self):
        query = self.entry.text().strip()
        if not query:
            self.text_area.setPlainText("Please enter a query.")
            return

        try:
            result = wikipedia.page(query)
            content = result.content
            filename = f"{query}_{languages[self.lang]}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            self.text_area.setPlainText(content)
            self.scroll_area.setVisible(False)

            if (query, self.lang) not in self.history:
                self.history.append((query, self.lang))
                self.history_list.addItem(f"{query} ({self.lang})")
            self.save_history()

        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            self.text_area.clear()
            self.text_area.setPlainText("Disambiguation options found. Select one:")

            for i in reversed(range(self.button_layout.count())):
                self.button_layout.itemAt(i).widget().setParent(None)

            for option in options:
                button = QPushButton(option)
                button.setStyleSheet("background-color:#5e81ac;color:#eceff4;border-radius:5px;padding:5px;")
                button.clicked.connect(lambda _, opt=option: self.open_in_browser(opt))
                self.button_layout.addWidget(button)

            self.scroll_area.setVisible(True)

        except wikipedia.exceptions.PageError:
            self.text_area.setPlainText("Nothing was found on Wikipedia.")
            self.scroll_area.setVisible(False)

    def open_in_browser(self, option):
        try:
            search_url = f"https://{languages[self.lang]}.wikipedia.org/wiki/{option.replace(' ', '_')}"
            webbrowser.open(search_url)
        except wikipedia.exceptions.DisambiguationError as e:
            search_url = f"https://{languages[self.lang]}.wikipedia.org/wiki/Special:Search?search={option.replace(' ', '+')}"
            webbrowser.open(search_url)
        except wikipedia.exceptions.PageError:
            self.text_area.setPlainText("Ошибка: Статья не найдена.")

    def handle_history_click(self, item):
        text = item.text()
        query, lang = text.rsplit(" ", 1)
        query = query.strip()
        lang = lang.strip("()")
        self.switch_language(lang)
        filename = f"{query}_{languages[lang]}.txt"
        if os.path.isfile(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.history_text_area.setPlainText(content)
        else:
            self.history_text_area.setPlainText("File not found.")

    def save_history(self):
        with open("previous_search.txt", "w", encoding="utf-8") as file:
            for query, lang in self.history:
                file.write(f"{query} ({lang})\n")

    def load_history(self):
        if os.path.isfile("previous_search.txt"):
            with open("previous_search.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if " (" in line and line.endswith(")\n"):
                        query, lang = line.rsplit(" ", 1)
                        query = query.strip()
                        lang = lang.strip("()\n")
                        self.history.append((query, lang))
                        self.history_list.addItem(f"{query} ({lang})")


    def closeEvent(self, event):
        self.save_history()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('wiki.ico'))
    main_window = WikipediaApp()
    main_window.setWindowIcon(QtGui.QIcon('wiki.ico'))
    main_window.load_history()
    main_window.show()
    sys.exit(app.exec_())
