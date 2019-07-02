import os
import pickle


def read_file(path):
    if os.path.exists(path):
        with open(path) as file:
            return [str(i)[: len(i) - 1] for i in file]


def write_file(path, text):
    with open(path, "w") as file:
        file.write(text + "\n")


def append_file(path, text):
    with open(path, "a") as file:
        file.write(text + "\n")


def read_binary_file(path):
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))


def append_binary_file(path, obj):
    if os.path.exists(path):
        data = read_binary_file(path)

        if not isinstance(data, list):
            raise Exception('Object saved in file is not a list')

        data.append(obj)
        write_file(path, data)


def write_binary_file(path, obj):
    pickle.dump(obj, open(path, "wb"))
