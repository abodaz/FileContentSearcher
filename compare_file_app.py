import os
import sys
import io
import pyperclip
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton, QScrollArea, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from contextlib import redirect_stdout


def get_user_input():
    user_input = input("Enter a list of strings separated by commas: ")
    return [item.strip() for item in user_input.split(",")]

def get_files_has_entered_word(word, directory_path):
    file_results = []
    try:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    if word in file_content:
                        file_results.append(file_path)
    except Exception as e:
        print(f"Error: {e}")

    return file_results

def get_files_has_element_or_more(elements, files):
    file_results = {}
    try:
        for file in files:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
                matched_elements = [element for element in elements if element in file_content]
                if matched_elements:
                    file_results[file] = matched_elements
    except Exception as e:
        print(f"An error occurred: {e}")
    return file_results

def capture_printed_output(func, *args, **kwargs):
    with io.StringIO() as output:
        with redirect_stdout(output):
            func(*args, **kwargs)
        printed_output = output.getvalue()
    return printed_output

def print_elements_found(elements, file_results):
    output = io.StringIO()
    for element in elements:
        files_with_element = [file for file, matched_elements in file_results.items() if element in matched_elements]
        if files_with_element:
            print(f"'{element}' exists in the following files:", file=output)
            for file in files_with_element:
                print(f"  - {file}", file=output)
        else:
            print(f"'{element}' does not exist in any file in the directory.", file=output)

    printed_output = output.getvalue()
    output.close()
    return printed_output

def print_files_with_elements(file_results):
    output = io.StringIO()
    print("\nFiles containing at least one not handled json fields", file=output)
    files_with_elements = []
    for file, matched_elements in file_results.items():
        files_with_elements.append(file)
        print(f"File: {file}", file=output)
        print("Contains elements:", file=output)
        for element in matched_elements:
            print(f"  - {element}", file=output)

    printed_output = output.getvalue()
    output.close()
    return printed_output

class MainWindow(QMainWindow):
    default_directory_path = "/Users/abdallah/Documents/work/Unily.AdvancedQueriesService/test/integration-tests/assets/raw-test-scripts/"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elements Finder App")

        # Set the default size of the application window
        self.resize(800, 600)
        # Optionally, set a minimum size
        self.setMinimumSize(800, 600)

        self.layout = QVBoxLayout()

        self.instructions = QLabel("The Directory Path: ")
        self.layout.addWidget(self.instructions)

        self.directory_field = QLineEdit()
        self.directory_field.setText(self.default_directory_path)
        self.layout.addWidget(self.directory_field)

        self.change_button = QPushButton("Change")
        self.change_button.clicked.connect(self.change_directory_path)
        self.layout.addWidget(self.change_button)

        self.input_field = QLineEdit()
        self.input_field.setText("author.profileUrl,organiser.profileUrl,location,metadata,openGraphSummary.content,openGraphSummary.results,siteOwners,sortOrder,topics,url.url,url.description,customMetadataSummary")
        self.layout.addWidget(self.input_field)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)

        self.instructions = QLabel("Enter elements (comma separated):")
        self.layout.addWidget(self.instructions)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

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
        self.result_layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def change_directory_path(self):
        self.default_directory_path = self.directory_field.text()

    def copy_to_clipboard(self):
        pyperclip.copy(self.input_field.text())

    def perform_search(self):
        elements = self.input_field.text().split(",")
        elements = [element.strip() for element in elements]  # Strip whitespace from elements
        directory_path = self.default_directory_path
        word = "jsonResponseFields:"

        files_has_word = get_files_has_entered_word(word, directory_path)
        file_results = get_files_has_element_or_more(elements, files_has_word)

        elements_in_files = print_elements_found(elements, file_results)
        files_with_elements = print_files_with_elements(file_results)

        # Update the result label
        self.result_label.setText(
            f"Summary of elements within different files:\n{elements_in_files}\n\n"
            f"Summary of files containing at least one element:\n{files_with_elements}"
        )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
