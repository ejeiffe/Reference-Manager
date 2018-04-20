import sys
import string

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from create_new_db import *
from db_controller import *
from article_dialog_class import *

class RefManWindow(QMainWindow):
    """Creates main window for reference manager"""
    def __init__(self):
        super().__init__()
        self.controller = DbController("references.db")
        #create dictionary to hold opened article dialogs (key = article_id)
        self.article_views = {}
        self.search_term = None
        
        self.setWindowTitle("Reference Manager")
        self.resize(300,100)
        self.create_main_window_layout()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.main_menu_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def create_main_window_layout(self):
        #inital layout of window showing main menu options
        self.new_article_button = QPushButton("Add New Article")
        self.view_all_button = QPushButton("View All Articles")
        self.search_button = QPushButton("Search Database")
        self.exit_button = QPushButton("Exit")

        self.main_menu_layout = QVBoxLayout()
        self.main_menu_layout.addWidget(self.new_article_button)
        self.main_menu_layout.addWidget(self.view_all_button)
        self.main_menu_layout.addWidget(self.search_button)
        self.main_menu_layout.addWidget(self.exit_button)
        
        self.main_menu_widget = QWidget()
        self.main_menu_widget.setLayout(self.main_menu_layout)

        #connections
        self.new_article_button.clicked.connect(self.new_article_clicked)
        self.view_all_button.clicked.connect(self.view_all_clicked)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.exit_button.clicked.connect(self.close)

    def new_article_clicked(self):
        self.create_new_article_layout() 
        self.stacked_layout.addWidget(self.new_article_widget)
        self.stacked_layout.setCurrentIndex(1)

    def view_all_clicked(self):
        self.results = self.controller.show_all_articles()
        if not self.results:
            no_results_message = QMessageBox()
            no_results_message.setWindowTitle("No Results")
            no_results_message.setText("No results found")
        else:
            self.create_results_layout(self.results)
            self.stacked_layout.addWidget(self.results_widget)
            self.stacked_layout.setCurrentIndex(1)

    def search_button_clicked(self):
        self.create_search_layout()
        self.stacked_layout.addWidget(self.search_widget)
        self.stacked_layout.setCurrentIndex(1)

    def create_new_article_layout(self):
        self.title_label_new = QLabel("Title:")
        self.authors_label_new = QLabel("Authors:")
        self.journal_label_new = QLabel("Journal:")
        self.year_label_new = QLabel("Year:")
        self.volume_label_new = QLabel("Volume:")
        self.issue_label_new = QLabel("Issue:")
        self.pages_label_new = QLabel("Pages:")
        self.dash_label_new = QLabel("-")
        self.filepath_label_new = QLabel("File Location:")
        self.keywords_label_new = QLabel("Keywords:")
        self.notes_label_new = QLabel("Notes:")

        self.title_line_edit_new = QLineEdit()
        self.title_line_edit_new.setFixedWidth(500)
        self.authors_text_edit_new = QTextEdit()
        self.authors_text_edit_new.setToolTip("Enter each author on a new line")
        self.journal_line_edit_new = QLineEdit()
        self.year_spin_box_new = QSpinBox()
        self.year_spin_box_new.setRange(0,9999)
        self.year_spin_box_new.setValue(2018)
        self.year_spin_box_new.setFixedWidth(80)
        self.volume_line_edit_new = QLineEdit()
        self.issue_line_edit_new = QLineEdit()
        self.first_page_line_edit_new = QLineEdit()
        self.last_page_line_edit_new = QLineEdit()
        self.filepath_line_edit_new = QLineEdit()
        self.filepath_line_edit_new.setToolTip("Include file extension (.pdf, .doc)")
        self.keywords_line_edit_new = QLineEdit()
        self.notes_line_edit_new = QLineEdit()
       
        self.submit_button_new = QPushButton("Submit")
        self.submit_button_new.setToolTip("Add article to database")
        self.return_button_new = QPushButton("Return to Main Menu")
        self.return_button_new.setToolTip("Article will not be saved")

        self.vol_iss_pages_layout = QHBoxLayout()
        self.vol_iss_pages_layout.addWidget(self.volume_line_edit_new)
        self.vol_iss_pages_layout.addWidget(self.issue_label_new)
        self.vol_iss_pages_layout.addWidget(self.issue_line_edit_new)
        self.vol_iss_pages_layout.addWidget(self.pages_label_new)
        self.vol_iss_pages_layout.addWidget(self.first_page_line_edit_new)
        self.vol_iss_pages_layout.addWidget(self.dash_label_new)
        self.vol_iss_pages_layout.addWidget(self.last_page_line_edit_new)

        self.article_grid_layout = QGridLayout()
        self.article_grid_layout.addWidget(self.title_label_new,0,0)
        self.article_grid_layout.addWidget(self.authors_label_new,1,0)
        self.article_grid_layout.addWidget(self.journal_label_new,2,0)
        self.article_grid_layout.addWidget(self.year_label_new,3,0)
        self.article_grid_layout.addWidget(self.volume_label_new,4,0)
        self.article_grid_layout.addWidget(self.filepath_label_new,5,0)
        self.article_grid_layout.addWidget(self.keywords_label_new,6,0)
        self.article_grid_layout.addWidget(self.notes_label_new,7,0)
        self.article_grid_layout.addWidget(self.title_line_edit_new,0,1)
        self.article_grid_layout.addWidget(self.authors_text_edit_new,1,1)
        self.article_grid_layout.addWidget(self.journal_line_edit_new,2,1)
        self.article_grid_layout.addWidget(self.year_spin_box_new,3,1)
        self.article_grid_layout.addLayout(self.vol_iss_pages_layout,4,1)
        self.article_grid_layout.addWidget(self.filepath_line_edit_new,5,1)
        self.article_grid_layout.addWidget(self.keywords_line_edit_new,6,1)
        self.article_grid_layout.addWidget(self.notes_line_edit_new,7,1)

        self.buttons_layout_new = QHBoxLayout()
        self.buttons_layout_new.addWidget(self.submit_button_new)
        self.buttons_layout_new.addWidget(self.return_button_new)

        self.new_article_layout = QVBoxLayout()
        self.new_article_layout.addLayout(self.article_grid_layout)
        self.new_article_layout.addLayout(self.buttons_layout_new)

        self.new_article_widget = QWidget()
        self.new_article_widget.setLayout(self.new_article_layout)
        self.new_article_widget.setAttribute(Qt.WA_DeleteOnClose, on=True)

        self.submit_button_new.clicked.connect(self.new_article_submit)
        self.return_button_new.clicked.connect(self.return_to_main_clicked)

    def new_article_values(self):
        #convert author names to correct format for database entry
        authors = []
        for author in self.authors_text_edit_new.toPlainText().split('\n'):
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
        #return all values as tuple
        return self.title_line_edit_new.text(), authors, \
        self.journal_line_edit_new.text(), self.year_spin_box_new.value(), \
        self.volume_line_edit_new.text(), self.issue_line_edit_new.text(), \
        self.first_page_line_edit_new.text(), self.last_page_line_edit_new.text(), \
        self.filepath_line_edit_new.text(), self.keywords_line_edit_new.text(), \
        self.notes_line_edit_new.text()

    def new_article_clear(self):
        self.title_line_edit_new.clear()
        self.authors_text_edit_new.clear()
        self.journal_line_edit_new.clear()
        self.year_spin_box_new.setValue(2018)
        self.volume_line_edit_new.clear()
        self.issue_line_edit_new.clear()
        self.first_page_line_edit_new.clear()
        self.last_page_line_edit_new.clear()
        self.filepath_line_edit_new.clear()
        self.keywords_line_edit_new.clear()
        self.notes_line_edit_new.clear()

    def new_article_submit(self):
        article_inputs = self.new_article_values()
        self.controller.new_article(*article_inputs)
        self.new_article_clear()

    def return_to_main_clicked(self):
        current_window = self.stacked_layout.currentWidget()
        self.stacked_layout.removeWidget(current_window)
        self.resize(300,100)
        current_window.close()

    def create_results_layout(self, results):
        self.first_author_heading = QLabel("<b>First Author\t</b>")
        self.year_heading = QLabel("<b>Year</b>")
        self.year_heading.setFixedWidth(70)
        self.journal_heading = QLabel("<b>Journal</b>")
        self.journal_heading.setFixedWidth(200)
        self.title_heading = QLabel("<b>Title</b>")
        self.title_heading.setFixedWidth(300)

        self.search_button_results = QPushButton("Search")
        self.return_to_main_results = QPushButton("Return to Main Menu")

        self.search_results_grid = QGridLayout()
        self.search_results_grid.addWidget(self.first_author_heading,0,0)
        self.search_results_grid.addWidget(self.year_heading,0,1)
        self.search_results_grid.addWidget(self.journal_heading,0,2)
        self.search_results_grid.addWidget(self.title_heading,0,3)

        #generating labels and button for each article found by search
        #creating dictionary to store article _id (key) with each view button (value)
        self.view_buttons = {}
        row = 1

        for entry in results:
            self.view_buttons[entry[0]] = QPushButton("View")
            self.search_results_grid.addWidget(QLabel(entry[1]),row,0)
            self.search_results_grid.addWidget(QLabel(str(entry[2])),row,1)
            self.search_results_grid.addWidget(QLabel(entry[3], wordWrap=True),row,2)
            self.search_results_grid.addWidget(QLabel(entry[4], wordWrap=True, minimumHeight=30),row,3)
            self.search_results_grid.addWidget(self.view_buttons[entry[0]],row,4)

            row += 1

        self.results_button_layout = QHBoxLayout()
        self.results_button_layout.addWidget(self.search_button_results)
        self.results_button_layout.addWidget(self.return_to_main_results)

        self.results_layout = QVBoxLayout()
        self.results_layout.addLayout(self.search_results_grid)
        self.results_layout.addLayout(self.results_button_layout)

        self.results_widget = QWidget()
        self.results_widget.setLayout(self.results_layout)
        self.results_widget.setAttribute(Qt.WA_DeleteOnClose, on=True)

        for article_id in self.view_buttons:
            self.view_buttons[article_id].clicked.connect(lambda _, a_id=article_id: self.view_button_clicked(article_id =a_id))

        self.search_button_results.clicked.connect(self.search_from_results)
        self.return_to_main_results.clicked.connect(self.return_to_main_clicked) 

    def view_button_clicked(self, article_id):
        try:
            self.article_views[article_id] = ArticleDialog(article_id)
            self.article_views[article_id].show()
        except:
            no_article_message = QMessageBox()
            no_article_message.setWindowTitle("Article Not Found")
            no_article_message.setText("Article not found. Please search again or return to the main menu.")
            no_article_message.exec_()


    def update_results(self):
        current_window = self.stacked_layout.currentWidget()
        self.stacked_layout.removeWidget(current_window)
        current_window.close() 
        self.create_results_layout(self.results)
        self.stacked_layout.addWidget(self.results_widget)
        self.stacked_layout.setCurrentIndex(1)
        
    def search_from_results(self):
        current_window = self.stacked_layout.currentWidget()
        self.stacked_layout.removeWidget(current_window)
        current_window.close()
        self.search_button_clicked()
        self.resize(300,100) 

    def create_search_layout(self):
        self.search_label = QLabel("Search by:")
        self.search_info_label = QLabel("Enter author surname")
        self.search_info_label.setWordWrap(True)
        self.search_info_label.setFixedHeight(60)

        self.search_line_edit = QLineEdit()

        self.search_run_button = QPushButton("Search")
        self.return_button_search = QPushButton("Return to Main Menu")

        self.search_dropdown = QComboBox()
        self.search_dropdown.addItem("Author")
        self.search_dropdown.addItem("Year")
        self.search_dropdown.addItem("Keyword")

        self.search_top_layout = QHBoxLayout()
        self.search_top_layout.addWidget(self.search_label)
        self.search_top_layout.addWidget(self.search_dropdown)

        self.search_button_layout = QHBoxLayout()
        self.search_button_layout.addWidget(self.search_run_button)
        self.search_button_layout.addWidget(self.return_button_search)

        self.search_layout = QVBoxLayout()
        self.search_layout.addLayout(self.search_top_layout)
        self.search_layout.addWidget(self.search_info_label)
        self.search_layout.addWidget(self.search_line_edit)
        self.search_layout.addLayout(self.search_button_layout)

        self.search_widget = QWidget()
        self.search_widget.setLayout(self.search_layout)
        self.search_widget.setAttribute(Qt.WA_DeleteOnClose, on=True)

        self.search_dropdown.activated[str].connect(self.search_input)

        self.search_run_button.clicked.connect(self.run_search)
        self.return_button_search.clicked.connect(self.return_to_main_clicked)

    def search_input(self, text):
        if text == "Year":
            self.search_info_label.setText("Enter a single year or use '-' to search over a range: e.g. 2000-2016, 2000- or -2016")
        elif text == "Author":
            self.search_info_label.setText("Enter author surname:")
        elif text == "Keyword":
            self.search_info_label.setText("Enter keyword (searches Title, Journal, Keywords and Notes): ")

    def run_search(self):
        search_term = self.search_line_edit.text()
        if self.search_dropdown.currentText() == "Author":
            self.results = self.controller.search_by_author(search_term.capitalize())
        elif self.search_dropdown.currentText() == "Year":
            if "-" in search_term:
                if search_term[0] == "-":
                    from_year = None
                    to_year = search_term.split("-")[1].strip()
                elif search_term[-1] == "-":
                    from_year = search_term.split("-")[0].strip()
                    to_year = None
                else:
                    from_year = search_term.split("-")[0]
                    to_year = search_term.split("-")[1]                
            else:
                from_year = search_term
                to_year = search_term
            try:
                if not to_year:
                    from_year = int(from_year)
                elif not from_year:
                    to_year = int(to_year)
                else:
                    from_year = int(from_year)
                    to_year = int(to_year)
            except:
                year_error_message = QMessageBox()
                year_error_message.setWindowTitle("Error")
                year_error_message.setText("Please enter each year as a four digit number")
                year_error_message.exec_()
                return False
            self.results = self.controller.search_by_year(from_year, to_year)
        elif self.search_dropdown.currentText() == "Keyword":
            self.results = self.controller.search_by_keyword(search_term)
        if not self.results:
            no_results_message = QMessageBox()
            no_results_message.setText("No results found")
            no_results_message.exec_()
        else:
            self.update_results()

      
if __name__ == "__main__":
    reference_manager = QApplication(sys.argv)
    main_window = RefManWindow()
    main_window.show()
    main_window.raise_()
    #creates new database when run for the first time
    if not os.path.exists("references.db"):
        create_new_db("references.db")
        new_db = QMessageBox()
        new_db.setWindowTitle("New Database")
        new_db.setText("New database created")
        new_db.exec_()
    reference_manager.exec_()
