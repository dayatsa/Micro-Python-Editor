from handler.FileHandler import *
import os


class LibraryHandler:

    @staticmethod
    def get_space_lib():
        text = "\n\n\n#============================ENDLIB=========================\n\n\n\n"
        return text


    @staticmethod
    def get_library_code(path):
        lib_data = ""
        list_dir = sorted(os.listdir(path))

        for dir in list_dir:
            print(dir)
            full_path = os.path.join(path, dir)
            data = FileHandler.open_file_with_name(full_path)
            lib_data += data
            lib_data += LibraryHandler.get_space_lib()
        
        return lib_data