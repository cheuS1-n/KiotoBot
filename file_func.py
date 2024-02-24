import os


def ReadOtherFile(File: str) -> str:
    with open(f"Data/Other/{File}", "r") as file:
        file1 = file.read()
    return file1
def WriteOtherFile(File: str, Value):
    with open(f"Data/Other/{File}", "w") as file:
        file.write(Value)
def get_file_names_in_directory(directory_path):
    file_names = []
    for file_name in os.listdir(directory_path):
        full_path = os.path.join(directory_path, file_name)
        if os.path.isfile(full_path):
            file_names.append(file_name)
    return file_names
def ReadtmpFile(File: str) -> str:
    with open(f"Data/tmp/{File}", "r") as file:
        file1 = file.read()
    return file1
def WritetmpFile(File: str, Value):
    with open(f"Data/tmp/{File}", "w") as file:
        file.write(Value)