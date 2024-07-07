import os
import io
from contextlib import redirect_stdout


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
    filenames = []
    for file, matched_elements in file_results.items():
        files_with_elements.append(file)
        filename = os.path.basename(file)
        filenames.append(filename)
        print(f"File: {file}", file=output)
        print("Contains elements:", file=output)
        for element in matched_elements:
            print(f"  - {element}", file=output)

    print("\nSummary of filenames:", file=output)
    for filename in filenames:
        print(filename, file=output)

    printed_output = output.getvalue()
    output.close()
    return printed_output, filenames
