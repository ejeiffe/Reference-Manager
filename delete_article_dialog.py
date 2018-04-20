from PyQt5.QtWidgets import *

from db_controller import *

class DeleteDialog(QDialog):

    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id
        self.controller = DbController("references.db")

        self.setWindowTitle("Delete Article")

        self.delete_message_label = QLabel("Are you sure you want to delete this article?")

        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)

        self.delete_dialog_layout = QVBoxLayout()
        self.delete_dialog_layout.addWidget(self.delete_message_label)
        self.delete_dialog_layout.addLayout(self.button_layout)

        self.setLayout(self.delete_dialog_layout)

        self.yes_button.clicked.connect(self.delete_article)
        self.no_button.clicked.connect(self.close)

    def delete_article(self):
        self.controller.delete_article(self.article_id)
        self.deleted = True
        self.confirmation_message = QMessageBox()
        self.confirmation_message.setWindowTitle("Article deleted")
        self.confirmation_message.setFixedWidth(250)
        self.confirmation_message.exec_()
        self.close()


