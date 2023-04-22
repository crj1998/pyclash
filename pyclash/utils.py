import os

def get_file_path(filename):
    module_location = os.path.dirname(os.path.abspath(__file__))
    parent_location = os.path.dirname(module_location)
    file_location = os.path.join(parent_location, filename)
    return file_location