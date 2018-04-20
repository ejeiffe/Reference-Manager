import string

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from db_controller import *

class AuthorsEditDialog(QDialog):
    """Creates a multi-page dialog box for adding, removing, editing or reordering article authors"""

    def __init__(self, article_id, authors):
        super().__init__()
        self.article_id = article_id
        self.authors = authors
        self.edited = False
        self.controller = DbController("references.db")

        self.setWindowTitle("Edit Authors")
        self.create_initial_layout()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.initial_widget)

        self.setLayout(self.stacked_layout)

    def create_initial_layout(self):
        self.authors_label = QLabel("Authors: ")

        self.add_author_button = QPushButton("Add Author(s)")
        self.remove_author_button = QPushButton("Remove Author(s)")
        self.edit_author_button = QPushButton("Edit Author Names")
        self.reorder_authors_button = QPushButton("Reorder Authors")
        self.initial_cancel_button = QPushButton("Cancel")

        self.authors_contents = QVBoxLayout()
        for author in self.authors:
            if author[2] == "":
                self.authors_contents.addWidget(QLabel(author[1]+" "+author[3]))
            else:
                self.authors_contents.addWidget(QLabel(author[1]+" "+author[2]+" "+author[3]))

        self.initial_top_layout = QHBoxLayout()
        self.initial_top_layout.addWidget(self.authors_label)
        self.initial_top_layout.addLayout(self.authors_contents)

        self.initial_layout = QVBoxLayout()
        self.initial_layout.addLayout(self.initial_top_layout)
        self.initial_layout.addWidget(self.add_author_button)
        self.initial_layout.addWidget(self.remove_author_button)
        self.initial_layout.addWidget(self.edit_author_button)
        self.initial_layout.addWidget(self.reorder_authors_button)
        self.initial_layout.addWidget(self.initial_cancel_button)

        self.initial_widget = QWidget()
        self.initial_widget.setLayout(self.initial_layout)

        self.add_author_button.clicked.connect(self.add_author_clicked)
        self.remove_author_button.clicked.connect(self.remove_author_clicked)
        self.edit_author_button.clicked.connect(self.edit_author_clicked)
        self.reorder_authors_button.clicked.connect(self.reorder_authors_clicked)
        self.initial_cancel_button.clicked.connect(self.close)

    def add_author_clicked(self):
        self.create_add_author_layout() 
        self.stacked_layout.addWidget(self.add_author_widget)
        self.stacked_layout.setCurrentIndex(1)

    def remove_author_clicked(self):
        self.create_remove_author_layout() 
        self.stacked_layout.addWidget(self.remove_author_widget)
        self.stacked_layout.setCurrentIndex(1)

    def edit_author_clicked(self):
        self.create_edit_author_layout() 
        self.stacked_layout.addWidget(self.edit_author_widget)
        self.stacked_layout.setCurrentIndex(1)

    def reorder_authors_clicked(self):
        self.create_reorder_authors_layout() 
        self.stacked_layout.addWidget(self.reorder_authors_widget)
        self.stacked_layout.setCurrentIndex(1)

    def create_add_author_layout(self):
        self.add_author_label = QLabel("Add Author(s):")

        self.add_author_text_edit = QTextEdit()
        self.add_author_text_edit.setToolTip("Enter each author on a new line")

        self.add_author_confirm_button = QPushButton("Add Authors")
        self.add_author_cancel_button = QPushButton("Cancel")

        self.add_author_top_layout = QGridLayout()
        self.add_author_top_layout.addWidget(self.authors_label,0,0)
        self.add_author_top_layout.addLayout(self.authors_contents,0,1)
        self.add_author_top_layout.addWidget(self.add_author_label,1,0)
        self.add_author_top_layout.addWidget(self.add_author_text_edit,1,1)

        self.add_author_button_layout = QHBoxLayout()
        self.add_author_button_layout.addWidget(self.add_author_confirm_button)
        self.add_author_button_layout.addWidget(self.add_author_cancel_button)

        self.add_author_layout = QVBoxLayout()
        self.add_author_layout.addLayout(self.add_author_top_layout)
        self.add_author_layout.addLayout(self.add_author_button_layout)

        self.add_author_widget = QWidget()
        self.add_author_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.add_author_widget.setLayout(self.add_author_layout)

        self.add_author_confirm_button.clicked.connect(self.add_author)
        self.add_author_cancel_button.clicked.connect(self.return_to_initial)

    def get_new_author_info(self):
        authors = []
        for author in self.add_author_text_edit.toPlainText().split('\n'):
            author = author.split()
            if author[0][-1] == ',':
                if len(author) >= 3:
                    middle = " ".join(author[2:])
                    middle = "".join(char for char in middle if char not in string.punctuation)
                elif len(author) == 2:
                    middle = ""
                first = author[1]
                last = author[0][:-1]
            else:
                if len(author) >= 3:
                    middle = " ".join(author[1:-1])
                    middle = "".join(char for char in middle if char not in string.punctuation)
                elif len(author) == 2:
                    middle = ""
                first = author[0]
                last = author[-1]
            authors.append((first, middle, last))
        return authors
        
    def add_author(self):
        new_authors = self.get_new_author_info()
        if len(new_authors) == 0:
            no_add_message = QMessageBox()
            no_add_message.setWindowTitle("No Input Data")
            no_add_message.setText("No new authors added")
            no_add_message.exec_()
            self.return_to_initial()
        else:
            position = len(self.authors) + 1
            for author in new_authors:
                self.controller.add_author(self.article_id, author, position)
                position += 1
            add_confirm_message = QMessageBox()
            add_confirm_message.setWindowTitle("Authors Added")
            add_confirm_message.setText("New authors added to database")
            add_confirm_message.exec_()
            self.edited = True
            self.return_to_initial()
            self.update_initial_layout()            

    def return_to_initial(self):
        current_window = self.stacked_layout.currentWidget()
        self.stacked_layout.removeWidget(current_window)
        current_window.close()

    def update_initial_layout(self):
        self.authors = self.controller.get_article_authors(self.article_id)
        QWidget().setLayout(self.stacked_layout)
        self.create_initial_layout()
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.initial_widget)
        self.setLayout(self.stacked_layout)

    def create_remove_author_layout(self):
        self.remove_author_label = QLabel("Select author(s) to remove: ", wordWrap=True)

        self.remove_confirm_button = QPushButton("Remove Author(s)")
        self.remove_cancel_button = QPushButton("Cancel")

        self.remove_author_list = QGridLayout()
        #create dictionary to store author_id (key) with check button (value)
        self.remove_author_check_buttons = {}
        row = 0
        for author in self.authors:
            if author[2] == "":
                self.remove_author_list.addWidget(QLabel(author[1]+" "+author[3]),row,0)
            else:
                self.remove_author_list.addWidget(QLabel(author[1]+" "+author[2]+" "+author[3]),row,0)
            self.remove_author_check_buttons[(author[0], author[4])] = QCheckBox()
            self.remove_author_list.addWidget(self.remove_author_check_buttons[(author[0], author[4])],row,1)
            row += 1

        self.remove_author_button_layout = QHBoxLayout()
        self.remove_author_button_layout.addWidget(self.remove_confirm_button)
        self.remove_author_button_layout.addWidget(self.remove_cancel_button)

        self.remove_author_layout = QVBoxLayout()
        self.remove_author_layout.addWidget(self.remove_author_label)
        self.remove_author_layout.addLayout(self.remove_author_list)
        self.remove_author_layout.addLayout(self.remove_author_button_layout)

        self.remove_author_widget = QWidget()
        self.remove_author_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.remove_author_widget.setLayout(self.remove_author_layout)

        self.remove_confirm_button.clicked.connect(self.remove_author)
        self.remove_cancel_button.clicked.connect(self.return_to_initial)

    def remove_author(self):
        removed = False
        for author_id, position in self.remove_author_check_buttons:
            if self.remove_author_check_buttons[(author_id, position)].isChecked():
                self.controller.remove_author(self.article_id, author_id, position)
                removed = True
        if removed:
            removed_confirm_message = QMessageBox()
            removed_confirm_message.setWindowTitle("Authors Removed")
            removed_confirm_message.setText("Selected authors removed from article")
            removed_confirm_message.exec_()
            self.edited = True
            self.return_to_initial()
            self.update_initial_layout()
        else:
            no_remove_message = QMessageBox()
            no_remove_message.setWindowTitle("No Input Data")
            no_remove_message.setText("No authors removed")
            no_remove_message.exec_()
            self.return_to_initial()

    def create_edit_author_layout(self):
        self.edit_author_label = QLabel("Edit Author Name(s):")

        self.edit_author_confirm_button = QPushButton("Save changes")
        self.edit_author_cancel_button = QPushButton("Cancel")

        self.edit_author_button_layout = QHBoxLayout()
        self.edit_author_button_layout.addWidget(self.edit_author_confirm_button)
        self.edit_author_button_layout.addWidget(self.edit_author_cancel_button)

        self.edit_author_layout = QVBoxLayout()
        self.edit_author_layout.addWidget(self.edit_author_label)

        #create dictionary to store author id (key) with author line edit (value)
        self.edit_author_line_edits = {}

        for author in self.authors:
            self.edit_author_line_edits[author[0]] = QLineEdit()
            if author[2] == "":
                self.edit_author_line_edits[author[0]].setText(author[1]+" "+author[3])
            else:
                self.edit_author_line_edits[author[0]].setText(author[1]+" "+author[2]+" "+author[3])
            self.edit_author_layout.addWidget(self.edit_author_line_edits[author[0]])

        self.edit_author_layout.addLayout(self.edit_author_button_layout)

        self.edit_author_widget = QWidget()
        self.edit_author_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.edit_author_widget.setLayout(self.edit_author_layout)

        self.edit_author_confirm_button.clicked.connect(self.edit_authors)
        self.edit_author_cancel_button.clicked.connect(self.return_to_initial)

    def edit_authors(self):
        author_edit = False
        for author_id in self.edit_author_line_edits:
            if self.edit_author_line_edits[author_id].isModified():
                author = self.edit_author_line_edits[author_id].text().split()
                if len(author) >= 3:
                    middle = " ".join(author[1:-1])
                    middle = "".join(char for char in middle if char not in string.punctuation)
                elif len(author) == 2:
                    middle = ""
                first = author[0]
                last = author[-1]
                author_name = (first, middle, last)
                self.controller.edit_author(author_id, author_name)
                author_edit = True
        if author_edit:
            edit_confirm_message = QMessageBox()
            edit_confirm_message.setWindowTitle("Authors Edited")
            edit_confirm_message.setText("Author name(s) updated")
            edit_confirm_message.exec_()
            self.edited = True
            self.return_to_initial()
            self.update_initial_layout()
        else:
            no_edit_message = QMessageBox()
            no_edit_message.setWindowTitle("No Changes")
            no_edit_message.setText("No changes made to author names")
            no_edit_message.exec_()
            self.return_to_initial()

    def create_reorder_authors_layout(self):
        self.reorder_authors_label = QLabel("Move author names up or down:")

        self.reorder_confirm_button = QPushButton("Save changes")
        self.reorder_cancel_button = QPushButton("Cancel")

        self.reorder_authors_list = QListWidget()
        self.reorder_authors_list.setDragDropMode(QAbstractItemView.InternalMove)

        #create dictionary to store author_id (key) and list widget item (value)
        self.reorder_authors_list_items = {}

        for author in self.authors:
            self.reorder_authors_list_items[author[0]] = QListWidgetItem()
            if author[2] == "":
                self.reorder_authors_list_items[author[0]].setText(author[1]+" "+author[3])
            else:
                self.reorder_authors_list_items[author[0]].setText(author[1]+" "+author[2]+" "+author[3])
            self.reorder_authors_list.addItem(self.reorder_authors_list_items[author[0]])

        self.reorder_button_layout = QHBoxLayout()
        self.reorder_button_layout.addWidget(self.reorder_confirm_button)
        self.reorder_button_layout.addWidget(self.reorder_cancel_button)

        self.reorder_authors_layout = QVBoxLayout()
        self.reorder_authors_layout.addWidget(self.reorder_authors_label)
        self.reorder_authors_layout.addWidget(self.reorder_authors_list)
        self.reorder_authors_layout.addLayout(self.reorder_button_layout)

        self.reorder_authors_widget = QWidget()
        self.reorder_authors_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.reorder_authors_widget.setLayout(self.reorder_authors_layout)

        self.reorder_confirm_button.clicked.connect(self.reorder_authors)
        self.reorder_cancel_button.clicked.connect(self.return_to_initial)

    def reorder_authors(self):
        reorder = False
        #create dictonary of author_id (key) with original position (value)
        old_author_positions = {}
        for author in self.authors:
            old_author_positions[author[0]] = author[4]
        #create dictionary of author_id (key) with new posiiton (value)
        new_author_positions = {}
        for author_id in self.reorder_authors_list_items:
            new_author_positions[author_id] = (self.reorder_authors_list.row(self.reorder_authors_list_items[author_id])+1)
        for author_id in new_author_positions:
            if new_author_positions[author_id] != old_author_positions[author_id]:
                self.controller.change_author_position(self.article_id, author_id, new_author_positions[author_id])
                reorder = True
        if reorder:
            reorder_confirm_message = QMessageBox()
            reorder_confirm_message.setWindowTitle("Authors Reordered")
            reorder_confirm_message.setText("Order of authors updated")
            reorder_confirm_message.exec_()
            self.edited = True
            self.return_to_initial()
            self.update_initial_layout()
        else:
            no_reorder_message = QMessageBox()
            no_reorder_message.setWindowTitle("No Changes")
            no_reorder_message.setText("No changes made to author order")
            no_reorder_message.exec_()
            self.return_to_initial()