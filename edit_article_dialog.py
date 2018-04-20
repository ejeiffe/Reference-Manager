from PyQt5.QtWidgets import *

from db_controller import *

class EditDialog(QDialog):
    """Creates dialog box for editing article data"""

    def __init__(self, article_id, old_data, field):
        super().__init__()
        self.article_id = article_id
        self.field = field
        self.old_data = old_data
        self.edited = False
        self.controller = DbController("references.db")

        self.setWindowTitle("Edit "+self.field)

        self.create_edit_layout()

        self.setLayout(self.edit_layout)

    def create_edit_layout(self):
        self.field_label = QLabel("Enter new "+self.field+":")
        self.field_input = QLineEdit()
        self.field_input.setText(self.old_data)
        self.field_input.setFixedWidth(500)

        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.addWidget(self.field_label)
        self.edit_layout.addWidget(self.field_input)
        self.edit_layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(lambda: self.save_changes(self.field_input.text(), self.old_data))
        self.cancel_button.clicked.connect(self.close)

    def save_changes(self, new_data, old_data):        
        if new_data != old_data:
            self.controller.edit_article(self.article_id, self.field, new_data)
            self.edited = True
        self.edit_confirmation()

    def edit_confirmation(self):
        if self.edited:
            edit_confirmation_message = QMessageBox()
            edit_confirmation_message.setWindowTitle("Article Edited")
            edit_confirmation_message.setText("Changes saved to database")
            edit_confirmation_message.exec_()
        else:
            no_change_message = QMessageBox()
            no_change_message.setWindowTitle("Article Edited")
            no_change_message.setText("New data matches stored data. No changes made.")
            no_change_message.exec_()
        self.close()

class YearEditDialog(EditDialog):
    """Create dialog box for editing uear (with spinbox for year input)"""

    def __init__(self, article_id, old_data, field="Year"):
        super().__init__(article_id, old_data, field)
        self.field = "Year"

    def create_edit_layout(self):
        self.field_label = QLabel("Enter new Year:")
        self.field_input = QSpinBox()
        self.field_input.setRange(0,9999)
        self.field_input.setValue(self.old_data)

        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.addWidget(self.field_label)
        self.edit_layout.addWidget(self.field_input)
        self.edit_layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(lambda: self.save_changes(self.field_input.text(), self.old_data))
        self.cancel_button.clicked.connect(self.close)

class VolIssPageEditDialog(EditDialog):
    """Create dialog box for editing volume, issue and pages"""

    def __init__(self, article_id, old_data, field="Volume, Issue, Pages"):
        super().__init__(article_id, old_data, field)
        self.field = ["Volume", "Issue", "FirstPage", "LastPage"]
        self.old_data_dict = dict(zip(self.field, self.old_data))

    def create_edit_layout(self):
        self.volume_label = QLabel("Volume:")
        self.issue_label = QLabel("Issue:")
        self.pages_label = QLabel("Pages:")
        self.dash_label = QLabel("-")

        self.volume_line_edit = QLineEdit()
        self.volume_line_edit.setText(self.old_data[0])
        self.issue_line_edit = QLineEdit()
        self.issue_line_edit.setText(self.old_data[1])
        self.first_page_line_edit = QLineEdit()
        self.first_page_line_edit.setText(self.old_data[2])
        self.last_page_line_edit = QLineEdit()
        self.last_page_line_edit.setText(self.old_data[3])

        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel")

        self.fields_layout = QGridLayout()
        self.fields_layout.addWidget(self.volume_label,0,0)
        self.fields_layout.addWidget(self.volume_line_edit,0,1)
        self.fields_layout.addWidget(self.issue_label,0,2)
        self.fields_layout.addWidget(self.issue_line_edit,0,3)
        self.fields_layout.addWidget(self.pages_label,1,0)
        self.fields_layout.addWidget(self.first_page_line_edit,1,1)
        self.fields_layout.addWidget(self.dash_label,1,2)
        self.fields_layout.addWidget(self.last_page_line_edit,1,3)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.addLayout(self.fields_layout)
        self.edit_layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.save_changes_multiple)
        self.cancel_button.clicked.connect(self.close)

    def save_changes(self, new_data, old_data, field):        
        if new_data != old_data:
            self.controller.edit_article(self.article_id, field, new_data)
            self.edited = True

    def save_changes_multiple(self):
        self.new_data_list = [self.volume_line_edit.text(), self.issue_line_edit.text(),
        self.first_page_line_edit.text(),self.last_page_line_edit.text()]
        self.new_data_dict = dict(zip(self.field,self.new_data_list))
        for field in self.field:
            self.save_changes(self.new_data_dict[field], self.old_data_dict[field], field)
        self.edit_confirmation()








