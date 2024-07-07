import os
import io
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
    # Capture printed output as a string
    with io.StringIO() as output:
        with redirect_stdout(output):
            func(*args, **kwargs)
        printed_output = output.getvalue()
    return printed_output


def print_elements_found(elements, file_results):
    # Print elements found in the directory
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
    # Print files and the elements they contain
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


def main():
    directory_path = "/Users/abdallah/Documents/work/Unily.AdvancedQueriesService/test/integration-tests/assets/raw-test-scripts/"
    word = "jsonResponseFields:"
    elements = get_user_input()
    # word = get_user_input()
    # directory_path = input("Enter the directory path to search: ")

    files_has_word = get_files_has_entered_word(word, directory_path)
    file_results = get_files_has_element_or_more(elements, files_has_word)

    elements_in_files = print_elements_found(elements, file_results)
    files_with_elements = print_files_with_elements(file_results)

    # Summary of file names
    print("\nSummary of elements within different files")
    print(elements_in_files)

    # Summary of file names
    print("\nSummary of files containing at least one element:")
    print(files_with_elements)

    # Optionally return data if needed elsewhere in your application
    return file_results


if __name__ == "__main__":
    main()

# path: C:\Users\AbdallahHMAlazami\source\repos\Unily.AdvancedQueriesService\test\integration-tests\assets\raw-test-scripts
# responss json fields not handled yet: author.profileUrl,organiser.profileUrl,location,metadata,openGraphSummary.content,openGraphSummary.results,siteOwners,sortOrder,topics,url.url,url.description,customMetadataSummary
# new responss json fields  will be handled:
