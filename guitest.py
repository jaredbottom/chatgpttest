import sqlalchemy
import sys

import pandas as pd

from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox,
                             QPushButton, QTextEdit, QVBoxLayout,
                             QTextEdit, QHBoxLayout, QLabel)


# TODO:
# write function to take paramerers from dictionary and return(?)
# a sqlalchemy connection. Alternatively, it might make sense to
# modify the read and load claims function to do this internally.



clientDictionary = {'Client1': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client2': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client3': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client4': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client5': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client6': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client7': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client8': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client9': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client10': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    'Client11': {'server': '<++>', 'database': '<++>', 'table': '<++>'},
                    }


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the dropdown box
        self.client_combo = QComboBox()
        self.client_combo.addItems([x for x in clientDictionary])

        # Create the labels
        self.input_label = QLabel('Claims:')
        self.input_label.setEnabled(False)
        self.output_label = QLabel('Output:')
        self.output_label.setEnabled(False)

        # Create the text areas
        self.input_text = QTextEdit()
        self.output_text = QTextEdit()

        # Create the buttons
        self.view_button = QPushButton('View Claims')
        self.load_button = QPushButton('Load Claims')

        # Create the layout and add the widgets
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.client_combo)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        layout.addLayout(input_layout)
        layout.addWidget(self.view_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        # Connect the buttons to their respective actions
        self.view_button.clicked.connect(self.view_claims)
        self.load_button.clicked.connect(self.load_claims)

        # Set the stylesheet for the disabled labels
        self.setStyleSheet("""
            QLabel[enabled="false"] {
                color: #666666;
            }
        """)

    def view_claims(self):
        client = self.client_combo.currentText()
        # Execute the SQL query and retrieve the data
        df = pd.read_sql(f'SELECT * FROM claims WHERE client="{client}"', conn)
        # Display the data in the text area
        self.output_text.setPlainText(str(df))
        self.output_label.setEnabled(True)

    def load_claims(self):
        client = self.client_combo.currentText()
        # Get the list of claims from the input text area
        claims = self.input_text.toPlainText().strip().split('\n')
        # Create a Pandas dataframe from the list of claims
        df = pd.DataFrame({'client': client, 'claim': claims})
        # Load the data into the database
        try:
            df.to_sql(name='claims', con=conn, if_exists='append', index=False)
            self.output_text.setPlainText('Claims loaded successfully!')
            self.output_label.setEnabled(True)
            self.input_label.setEnabled(False)
        except Exception as e:
            self.output_text.setPlainText(f'Error: {e}')
            self.output_label.setEnabled(True)
            self.input_label.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
