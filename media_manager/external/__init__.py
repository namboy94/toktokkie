import os


def get_location(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
