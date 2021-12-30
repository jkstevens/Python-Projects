import os


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def read_files(directory_path: str) -> list[str]:
    file_contents = []
    file_paths = list(os.listdir(directory_path))
    for i, file_path in enumerate(file_paths):
        if i % 100 == 0:
            print("\rReading file", i + 1, "/", len(file_paths), end='')
        file_contents.append(read_file(directory_path + "/" + file_path))
    print("\rRead", len(file_paths), "files.                ")
    return file_contents
