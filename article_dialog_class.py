import os.path

from PyQt5.QtWidgets import *

from db_controller import *
from delete_article_dialog import *
from edit_article_dialog import *
from edit_authors_dialog import *

class ArticleDialog(QDialog):
    """Creates dialog window showing article details"""
    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id
        self.controller = DbController("references.db")
        
        self.setWindowTitle("Article Details")
        self.create_article_layout()

        self.setLayout(self.article_layout)

    def create_article_layout(self):
        self.title_label = QLabel("Title:")
        self.authors_label = QLabel("Authors:")
        self.journal_label = QLabel("Journal:")
        self.year_label = QLabel("Year:")
        self.volume_label = QLabel("Volume:")
        self.issue_label = QLabel("Issue:")
        self.pages_label = QLabel("Pages:")
        self.filepath_label = QLabel("File Location:")
        self.keywords_label = QLabel("Keywords:")
        self.notes_label = QLabel("Notes:")

        (self.title, self.authors, self.journal, self.year, 
            self.volume, self.issue, self.first_page, self.last_page, 
            self.file_path, self.keywords, self.notes) = self.controller.display_article(self.article_id)

        self.title_contents = QLabel(self.title, wordWrap=True)
        self.title_contents.setFixedWidth(300)
        self.journal_contents = QLabel(self.journal, wordWrap=True)
        self.year_contents = QLabel(str(self.year))
        self.volume_contents = QLabel(self.volume)
        self.issue_contents = QLabel(self.issue)
        self.pages_contents = QLabel(self.first_page+"-"+self.last_page)
        self.filepath_contents = QLabel(self.file_path, wordWrap=True)
        self.filepath_contents.setFixedWidth(300)
        self.keywords_contents = QLabel(self.keywords, wordWrap=True)
        self.notes_contents = QLabel(self.notes, wordWrap=True)

        self.title_edit_button = QPushButton("Edit")
        self.authors_edit_button = QPushButton("Edit")
        self.journal_edit_button = QPushButton("Edit")
        self.year_edit_button = QPushButton("Edit")
        self.vol_iss_page_edit_button = QPushButton("Edit")
        self.filepath_edit_button = QPushButton("Edit")
        self.keywords_edit_button = QPushButton("Edit")
        self.notes_edit_button = QPushButton("Edit")

        self.open_file_button = QPushButton("Open File")
        self.delete_article_button = QPushButton("Delete Article")
        self.close_button = QPushButton("Close Window")

        #authors is a list of tuples of the form (first name, middle initial, surname)
        self.authors_contents = QVBoxLayout()
        for author in self.authors:
            if author[2] == "":
                self.authors_contents.addWidget(QLabel(author[1]+" "+author[3]))
            else:
                self.authors_contents.addWidget(QLabel(author[1]+" "+author[2]+" "+author[3]))

        self.vol_iss_page_layout = QHBoxLayout()
        self.vol_iss_page_layout.addWidget(self.volume_contents)
        self.vol_iss_page_layout.addWidget(self.issue_label)
        self.vol_iss_page_layout.addWidget(self.issue_contents)
        self.vol_iss_page_layout.addWidget(self.pages_label)
        self.vol_iss_page_layout.addWidget(self.pages_contents)
        
        self.article_grid_layout = QGridLayout()
        self.article_grid_layout.addWidget(self.title_label,0,0)
        self.article_grid_layout.addWidget(self.title_contents,0,1)
        self.article_grid_layout.addWidget(self.title_edit_button,0,2)
        self.article_grid_layout.addWidget(self.authors_label,1,0)
        self.article_grid_layout.addLayout(self.authors_contents,1,1)
        self.article_grid_layout.addWidget(self.authors_edit_button,1,2)
        self.article_grid_layout.addWidget(self.journal_label,2,0)
        self.article_grid_layout.addWidget(self.journal_contents,2,1)
        self.article_grid_layout.addWidget(self.journal_edit_button,2,2)
        self.article_grid_layout.addWidget(self.year_label,3,0)
        self.article_grid_layout.addWidget(self.year_contents,3,1)
        self.article_grid_layout.addWidget(self.year_edit_button,3,2)
        self.article_grid_layout.addWidget(self.volume_label,4,0)
        self.article_grid_layout.addLayout(self.vol_iss_page_layout,4,1)
        self.article_grid_layout.addWidget(self.vol_iss_page_edit_button,4,2)
        self.article_grid_layout.addWidget(self.filepath_label,5,0)
        self.article_grid_layout.addWidget(self.filepath_contents,5,1)
        self.article_grid_layout.addWidget(self.filepath_edit_button,5,2)
        self.article_grid_layout.addWidget(self.keywords_label,6,0)
        self.article_grid_layout.addWidget(self.keywords_contents,6,1)
        self.article_grid_layout.addWidget(self.keywords_edit_button,6,2)
        self.article_grid_layout.addWidget(self.notes_label,7,0)
        self.article_grid_layout.addWidget(self.notes_contents,7,1)
        self.article_grid_layout.addWidget(self.notes_edit_button,7,2)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.open_file_button)
        self.buttons_layout.addWidget(self.delete_article_button)
        self.buttons_layout.addWidget(self.close_button)

        self.article_layout = QVBoxLayout()
        self.article_layout.addLayout(self.article_grid_layout)
        self.article_layout.addLayout(self.buttons_layout)

        #add connections for edit buttons
        self.title_edit_button.clicked.connect(lambda: self.edit_field(self.title, "Title"))
        self.authors_edit_button.clicked.connect(self.edit_authors)
        self.journal_edit_button.clicked.connect(lambda: self.edit_field(self.journal, "Journal"))
        self.year_edit_button.clicked.connect(self.edit_year)
        self.vol_iss_page_edit_button.clicked.connect(self.edit_vol_iss_pages)
        self.filepath_edit_button.clicked.connect(lambda: self.edit_field(self.file_path, "FilePath"))
        self.keywords_edit_button.clicked.connect(lambda: self.edit_field(self.keywords, "Keywords"))
        self.notes_edit_button.clicked.connect(lambda: self.edit_field(self.notes, "Notes"))

        self.open_file_button.clicked.connect(self.open_file)
        self.delete_article_button.clicked.connect(self.open_delete_dialog)
        self.close_button.clicked.connect(self.close)

    def open_file(self):
        path = self.controller.get_path(self.article_id)
        if path == "":
            no_path_message = QMessageBox()
            no_path_message.setWindowTitle("File not found")
            no_path_message.setText("No file location provided")
            no_path_message.exec_()
        else:
            try:
                os.startfile(path)
            except:
                not_found_message = QMessageBox()
                not_found_message.setWindowTitle("File not found")
                not_found_message.setText("Please check the file location")
                not_found_message.exec_()

    def open_delete_dialog(self):
        self.delete_article_dialog = DeleteDialog(self.article_id)
        self.delete_article_dialog.exec_()
        if self.delete_article_dialog.deleted:
            self.close()

    def edit_field(self, old_data, field):
        edit_dialog = EditDialog(self.article_id, old_data, field)
        edit_dialog.exec_()
        if edit_dialog.edited:
            self.update_status()

    def edit_year(self):
        edit_dialog = YearEditDialog(self.article_id, self.year)
        edit_dialog.exec_()
        if edit_dialog.edited:
            self.update_status()

    def edit_vol_iss_pages(self):
        edit_dialog = VolIssPageEditDialog(self.article_id, old_data=[self.volume, self.issue, self.first_page, self.last_page])
        edit_dialog.exec_()
        if edit_dialog.edited:
            self.update_status()

    def edit_authors(self):
        edit_dialog = AuthorsEditDialog(self.article_id, self.authors)
        edit_dialog.exec()
        if edit_dialog.edited:
            self.edited = True
            self.update_status()

    def update_status(self):
        QWidget().setLayout(self.article_layout)
        self.create_article_layout()
        self.setLayout(self.article_layout)



    





