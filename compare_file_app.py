import sys
import pyperclip
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, \
    QLineEdit, QHBoxLayout, QTextEdit

# Import the helper functions from the file_operations.py script
from file_operations import (
    get_files_has_entered_word,
    get_files_has_element_or_more,
    print_elements_found,
    print_files_with_elements
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Element Finder App")

        # Set the default size of the application window
        self.resize(1200, 900)
        # Optionally, set a minimum size
        self.setMinimumSize(800, 600)

        self.default_directory_path = "/Users/abdallah/Documents/work/Unily.AdvancedQueriesService/test/integration-tests/assets/raw-test-scripts/"
        self.default_word_condition = "jsonResponseFields:"
        self.layout = QVBoxLayout()
        # Horizontal layout for the input field and copy button
        self.input_layout1 = QHBoxLayout()

        self.instructions = QLabel("The Directory Path: ")
        self.layout.addWidget(self.instructions)

        self.directory_field = QLineEdit()
        self.directory_field.setText(self.default_directory_path)
        self.input_layout1.addWidget(self.directory_field)

        self.change_button = QPushButton("Change")
        self.change_button.clicked.connect(self.change_directory_path)
        self.input_layout1.addWidget(self.change_button)

        self.layout.addLayout(self.input_layout1)

        self.input_layout2 = QHBoxLayout()

        self.condition = QLabel("Having Common Word: ")
        self.input_layout2.addWidget(self.condition)

        self.directory_field = QLineEdit()
        self.directory_field.setText(self.default_word_condition)
        self.input_layout2.addWidget(self.directory_field)

        self.change_button = QPushButton("Change")
        self.change_button.clicked.connect(self.change_condition_word)
        self.input_layout2.addWidget(self.change_button)

        self.layout.addLayout(self.input_layout2)

        # Horizontal layout for the input field and copy button
        self.input_layout3 = QHBoxLayout()
        self.input_field = QLineEdit()

        self.instructions = QLabel("Enter elements (comma separated):")
        self.layout.addWidget(self.instructions)

        self.input_field.setText(
            "author.profileUrl,organiser.profileUrl,location,metadata,openGraphSummary.content,openGraphSummary.results,siteOwners,sortOrder,topics,url.url,url.description,customMetadataSummary")
        self.input_layout3.addWidget(self.input_field)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.input_layout3.addWidget(self.copy_button)

        self.layout.addLayout(self.input_layout3)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)

        self.result_area = QScrollArea()
        self.result_content = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_content.setLayout(self.result_layout)
        self.result_area.setWidget(self.result_content)
        self.result_area.setWidgetResizable(True)
        self.layout.addWidget(self.result_area)

        self.result_label = QLabel("Results will be shown here")
        self.result_field = QLineEdit()
        self.result_field.setText("Results to copy will show here")
        self.result_layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_field)

        # Input fields for two lists of elements
        self.input_layout3 = QHBoxLayout()
        self.instructions2 = QLabel("Enter the first list of files (comma separated):")
        self.input_layout3.addWidget(self.instructions2)
        self.input_field1 = QLineEdit()
        self.input_layout3.addWidget(self.input_field1)
        self.layout.addLayout(self.input_layout3)

        self.input_layout5 = QHBoxLayout()
        self.instructions3 = QLabel("Enter the second list of files (comma separated):")
        self.input_layout5.addWidget(self.instructions3)
        self.input_field2 = QLineEdit()
        self.input_layout5.addWidget(self.input_field2)
        self.layout.addLayout(self.input_layout5)

        # Button to perform comparison
        self.compare_button = QPushButton("Compare Lists")
        self.compare_button.clicked.connect(self.compare_lists)
        self.layout.addWidget(self.compare_button)

        # Display area for results
        self.result_area2 = QTextEdit()
        self.result_area2.setReadOnly(True)
        self.layout.addWidget(self.result_area2)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def copy_to_clipboard(self):
        pyperclip.copy(self.input_field.text())

    def change_directory_path(self):
        self.default_directory_path = self.directory_field.text()

    def change_condition_word(self):
        self.default_word_condition = self.directory_field.text()

    def perform_search(self):
        elements = self.input_field.text().split(",")
        elements = [element.strip() for element in elements]  # Strip whitespace from elements

        files_has_word = get_files_has_entered_word(self.default_word_condition, self.default_directory_path)
        file_results = get_files_has_element_or_more(elements, files_has_word)

        elements_in_files = print_elements_found(elements, file_results)
        files_with_elements, filenames = print_files_with_elements(file_results)

        # Update the result label
        self.result_label.setText(
            f"Summary of elements within different files:\n{elements_in_files}\n\n"
            f"Summary of files containing at least one element:\n{files_with_elements}"
        )

        filenames = f"{', '.join(filenames)}"
        self.result_field.setText(filenames)

    def compare_lists(self):
        # Get input from the input fields
        array1 = self.input_field1.text().split(',')
        array2 = self.input_field2.text().split(',')

        # Trim whitespace from each element
        array1 = [element.strip() for element in array1]
        array2 = [element.strip() for element in array2]

        # Compare the arrays
        similar_elements, non_similar_elements1, non_similar_elements2 = self.compare_arrays(array1, array2)

        # Format the results
        result_text = f"Similar elements: {', '.join(similar_elements)}\n\n"
        result_text += f"Elements in first list but not in second list: {', '.join(non_similar_elements1)}\n\n"
        result_text += f"Elements in second list but not in first list: {', '.join(non_similar_elements2)}"

        # Display results in the result area
        self.result_area2.setText(result_text)

    def compare_arrays(self, array1, array2):
        set1 = set(array1)
        set2 = set(array2)

        similar_elements = list(set1.intersection(set2))
        non_similar_elements1 = list(set1.difference(set2))
        non_similar_elements2 = list(set2.difference(set1))

        return similar_elements, non_similar_elements1, non_similar_elements2


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
