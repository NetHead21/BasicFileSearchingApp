import os
import collections
import time

SearchResult = collections.namedtuple("SearchResult", "file, line, text")


def main():
    print_header()
    folder: str = get_folder_from_user()
    search_text: str = get_search_text_from_user()
    start = time.perf_counter()
    matches: list = search_folder(folder, search_text)


    for match in matches:
        print("-----MATCH-----")
        print(f"File: {match.file}")
        print(f"Line: {match.line}")
        print(f"Match: {match.text.strip()}")
        print()

    print(f"Finish at {time.perf_counter() - start} seconds.")


def print_header():
    print("-" * 15)
    print("FILE SEARCHING APP")
    print("-" * 15)


def get_folder_from_user() -> str:
    while True:
        if folder := input("What folder do you want to search?: ").strip():
            if os.path.isdir(folder):
                return os.path.abspath(folder)
            else:
                print("Folder doesn't exists!!!")
        else:
            print("Please enter a valid folder name!!!")


def get_search_text_from_user() -> str:
    while True:
        if search_text := input("What are you searching for?: ").strip():
            return search_text.lower()
        else:
            print("Please enter a valid search phrase!!!")


def search_folder(folder: str, search_for: str) -> list:
    items = os.listdir(folder)

    for item in items:
        full_item = os.path.join(folder, item)
        if os.path.isdir(full_item):
            yield from search_folder(full_item, search_for)
        else:
            yield from search_file(full_item, search_for)


def search_file(filename: str, search_text: str) -> list:
    with open(filename, "r", encoding="utf-8") as file_reader:
        line_num: int = 0
        for line in file_reader:
            line_num += 1
            if line.lower().find(search_text) >= 0:
                yield SearchResult(line=line_num, file=filename, text=line)


if __name__ == "__main__":
    main()
